from decimal import Decimal

from rest_framework.response  import Response


from common_libraries.cryptoapis.cryptoapis_utils import CryptoApisUtils
from common_libraries.constants.comissions import REAL_RECEIVING_PERCENTAGE

from common_libraries.emails.email_client import EmailClient

from assets.models import Asset
from api_keys.models import ApiKey
from digital_currency.models import DigitalCurrency
from cryptocurrency.models import Cryptocurrency, Blockchain, Network
from transactions.models import Transaction


from common_libraries.constants.cryptocurrency import CRYPTOCURRENCY_NETWORKS
from common_libraries.cryptoapis.cryptoapis_utils import CryptoApis



class TransactionUtils:
    def __init__(self):
        pass

    def create_transaction_digital_to_crypto(self, api_key, data):
        description = data["description"]
        digital_currency_code = data["digital_currency_code"]
        digital_currency_amount = data["digital_currency_amount"]
        cryptocurrency_code = data["cryptocurrency_code"]
        cryptocurrency_blockchain_id = data["cryptocurrency_blockchain_id"]
        withdrawal_address = data.get("withdrawal_address", None)
        customer_email = data.get("customer_email", None)
        customer_phone = data.get("customer_phone", None)

        """
            STEPS TO CREATE A TRANSACTION

            GET API KEY OBJECT
            GET DIGITAL CURRENCY OBJECT
            DEFINE TRANSACTION TYPE
            GENERATE ADDRESS
            CREATE TRANSACTION
        
        """

        api_key_object = ApiKey.objects.get(api_key = api_key)

        digital_currency_object =  DigitalCurrency.objects.get(digital_currency_id = digital_currency_code)

        # print(api_key_object.type, cryptocurrency_code)
        network_object = Network.objects.get(network_id = CRYPTOCURRENCY_NETWORKS[api_key_object.type][cryptocurrency_code])
        blockchain_object = Blockchain.objects.get(blockchain_id = cryptocurrency_blockchain_id)

        cryptocurrency_object = Cryptocurrency.objects.get(
            blockchain_id = blockchain_object,
            network_id = network_object,
            symbol = cryptocurrency_code
        )

        if cryptocurrency_object.cryptoapis_type == "ADDRESS":
            if not withdrawal_address:
                response_object = {
                    "status": "ERROR",
                    "error": "Missing withdrawal address"
                }

        # print(cryptocurrency_object.__dict__)
        # GENERATE ADDRESS
        cryptoapis_utils = CryptoApisUtils()
        address_object, error = cryptoapis_utils.generate_address(cryptocurrency_object, api_key_object)
        if error is not None:
            response_object = {
                "status": "ERROR",
                "message": error
            }
            return response_object


        """
        TRANSACTION TYPES

        - PAYMENT_REQUEST
        """

        digital_currency_amount_usd = Decimal(digital_currency_amount) / digital_currency_object.exchange_rate 

        cryptocurrency_amount = digital_currency_amount_usd / cryptocurrency_object.exchange_rate

        # MISSING REFUND ADDRESS
        new_transaction = Transaction.objects.create(
            api_key = api_key_object,
            type = "PAYMENT_REQUEST",
            description = description,
            digital_currency_id = digital_currency_object,
            digital_currency_amount = digital_currency_amount,
            cryptocurrency_amount = cryptocurrency_amount,
            address_id = address_object,
            client_email = customer_email if customer_email else None,
            client_phone = customer_phone if customer_phone else None,
            state = "PENDING",
            status = "WAITING_FOR_DEPOSIT"
        )

        response_object = {
            "status": "SUCCESS",
            "message": "Transaction created successfully",
            "data": {
                "transaction_id": new_transaction.transaction_id,
                "cryptocurrency_code": cryptocurrency_code,
                "deposit_crypto_address": address_object.address,
                "deposit_crypto_amount": cryptocurrency_amount,
                "expiration_timestamp": new_transaction.expiration_datetime.timestamp(),
                "creation_timestamp": new_transaction.creation_datetime.timestamp(),
                "payment_url": f"https://cryptosharepay.com/transactions/payments/{new_transaction.transaction_id}"
            }
        }

        return response_object

    def create_transaction_withdrawal(self, api_key_object, cryptocurrency_object, withdrawal_address, cryptocurrency_amount, source_address = None):

        asset = Asset.objects.get(
            api_key = api_key_object,
            cryptocurrency_id = cryptocurrency_object
        )

        if asset.amount < cryptocurrency_amount:
            return "Insufficient funds" # 402

        cryptoapis_utils = CryptoApisUtils()
        
        if cryptocurrency_object.type == "COIN":
            error = cryptoapis_utils.withdraw_coin_transaction_funds(cryptocurrency_object, withdrawal_address, cryptocurrency_amount, source_address = source_address)
            if error is not None:
                return error
            

        elif cryptocurrency_object.type == "ERC-20":
            if source_address is None:
                return "Withdrawals are not currently supported for this cryptocurrency" # 409

            error = cryptoapis_utils.withdraw_token_transaction_funds(source_address, cryptocurrency_object, withdrawal_address, cryptocurrency_amount)
            if error is not None:
                return error
        else:
            error = "Withdrawals are not currently supported for this cryptocurrency" # 409


        asset.amount -= Decimal(cryptocurrency_amount)
        asset.save()

        return None

    def create_transaction_payout_digital_to_crypto(self, api_key, data):
        
        pass

    def complete_transaction(self, transaction, api_key_object):
        ### TAX TAX TAX ###
        ### TAX TAX TAX ###
        
        receiving_amount = transaction.cryptocurrency_amount_received * REAL_RECEIVING_PERCENTAGE

        ### TAX TAX TAX ###
        ### TAX TAX TAX ###

        address_object = transaction.address_id
        cryptocurrency_object = address_object.cryptocurrency_id

        asset_object = Asset.objects.filter(api_key = api_key_object, cryptocurrency_id = cryptocurrency_object)
        if asset_object.exists():
            asset_object = asset_object.first()
            asset_object.amount += receiving_amount
            asset_object.save()
        else:
            asset_object = Asset.objects.create(
                api_key = api_key_object,
                type = cryptocurrency_object.type,
                amount = receiving_amount,
                cryptocurrency_id = cryptocurrency_object
            )
        
        if transaction.type == "PAYMENT_REQUEST":
            # MAKE ADDRESS AVAILABLE
            cryptoapis_utils = CryptoApisUtils()
            error = cryptoapis_utils.release_address(address_object)
            if error is not None:
                return error

            if cryptocurrency_object.type == "COIN":
                if transaction.withdrawal_address is not None:
                    # IF WITHDRAWAL ADDRESS WAS SPECIFIED
                    error = cryptoapis_utils.withdraw_coin_transaction_funds(cryptocurrency_object, transaction.withdrawal_address, receiving_amount, source_address = transaction.address_id.address)
                    if error is not None:
                        return error
                    else:
                        asset_object.amount -= receiving_amount
                        asset_object.save()

            elif cryptocurrency_object.type == "ERC-20":
                if transaction.withdrawal_address is not None:
                    error = cryptoapis_utils.withdraw_token_transaction_funds(transaction.address_id.address, cryptocurrency_object, transaction.withdrawal_address, receiving_amount)
                    if error is not None:
                        return error
                    else:
                        asset_object.amount -= receiving_amount
                        asset_object.save()

        transaction.state = "COMPLETE"
        transaction.status = "COMPLETED"
        transaction.expiration_datetime = None
        transaction.save()

        # SEND EMAIL
        email_client = EmailClient()
        email_client.complete_transaction(transaction, str(transaction.api_key.user_id.email))

        return None

    def cancel_transaction(self, transaction):
        transaction_address_object = transaction.address_id

        cryptoapis_utils = CryptoApisUtils()
        error = cryptoapis_utils.release_address(transaction_address_object)
        if error is not None:
            return error

        transaction.state = "CANCELLED"
        transaction.status = "CANCELLED"
        transaction.expiration_datetime = None
        transaction.save()

        return None

    def expired_transaction(self, transaction):
        transaction_address_object = transaction.address_id

        cryptoapis_utils = CryptoApisUtils()
        error = cryptoapis_utils.release_address(transaction_address_object)
        if error is not None:
            return error

        transaction.state = "CANCELED"
        transaction.status = "EXPIRED"
        transaction.expiration_datetime = None
        transaction.save()

        return None
    
    def cancel_automated_transaction(self, transaction):

        if transaction.funds_source_type == "DEPOSIT_ADDRESS":
            transaction_static_address_object = transaction.funds_source_address_object
            transaction_address_object = transaction_static_address_object.address_id

            cryptoapis_utils = CryptoApisUtils()
            error = cryptoapis_utils.release_address(transaction_address_object)
            if error is not None:
                return error

            transaction.funds_source_address = transaction.funds_source_address_object.address_id.address
            transaction.funds_source_address_object = None
            transaction.save()

            transaction_static_address_object.delete()

        transaction.status = "CANCELLED"
        transaction.save()

        return None
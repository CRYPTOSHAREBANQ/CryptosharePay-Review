from common_libraries.cryptoapis.cryptoapis_utils import CryptoApisUtils
from common_libraries.constants.comissions import REAL_RECEIVING_PERCENTAGE

from common_libraries.emails.email_client import EmailClient

from assets.models import Asset


class TransactionUtils:
    def __init__(self):
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
                    error = cryptoapis_utils.withdraw_coin_transaction_funds(transaction, cryptocurrency_object, transaction.withdrawal_address, receiving_amount)
                    if error is not None:
                        return error
                    else:
                        asset_object.amount -= receiving_amount
                        asset_object.save()

            elif cryptocurrency_object.type == "ERC-20":
                if transaction.withdrawal_address is not None:
                    error = cryptoapis_utils.withdraw_token_transaction_funds(transaction, cryptocurrency_object, transaction.withdrawal_address, receiving_amount)
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
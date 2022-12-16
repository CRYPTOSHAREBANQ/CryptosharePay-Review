# from atm_functions.models import Cryptocurrency, Address
from cryptocurrency.models import Address, AddressSubscription, Cryptocurrency, StaticAddress

from django.utils import timezone
from datetime import timedelta
from .cryptoapis import CryptoApis

class CryptoApisUtils:
    def generate_address(self, cryptocurrency_object, api_key_object):
        error = None

        """
            STEPS FOR GENERATING AN ADDRESS

            VERIFY ANY AVAILABLE ADDRESS IN DB
            IF NOT AVAILABLE:
                - GENERATE ADDRESS IN CRYPTOAPIS
                - GENERATE SUBSCRIPTION IN CRYPTOAPIS
                - SAVE ADDRESS IN DB
            IF AVAILABLE:
                - RETURN ADDRESS
        """
        
        """
            ADDRESSES STATUS

            - AVAILABLE
            - IN_USE
        """
        available_addresses = Address.objects.filter(
            cryptocurrency_id = cryptocurrency_object,
            status = "AVAILABLE"
        )

        if available_addresses.count() != 0:
            new_address = available_addresses.first()
            new_address.api_key = api_key_object
            new_address.status = "IN_USE"
            new_address.save()

        elif available_addresses.count() == 0:
            cryptoapis_client = CryptoApis(cryptocurrency_object.network_id.network_id)

            number_of_addresses = Address.objects.filter(cryptocurrency_id = cryptocurrency_object).count()

            try:
                deposit_address = cryptoapis_client.generate_deposit_address(
                    cryptocurrency_object.blockchain_id.blockchain_id, 
                    cryptocurrency_object.network_id.network_id, 
                    number_of_addresses,
                    api_key_object.type
                )
            except:
                error = "Error generating address. Please try again later."
                return None, error

            new_address = Address.objects.create(
                address_id = f"cryptosharepay|{api_key_object.type}|{cryptocurrency_object.blockchain_id.blockchain_id}|{cryptocurrency_object.network_id.network_id}|{number_of_addresses}",
                address = deposit_address,
                api_key = api_key_object,
                cryptocurrency_id = cryptocurrency_object,
                status = "IN_USE"
            )

        if new_address.subscription_id is None:
            cryptoapis_client = CryptoApis(cryptocurrency_object.network_id.network_id)

            try:
                if cryptocurrency_object.type == "ERC-20" or cryptocurrency_object.type == "TRC-20":
                    new_subscription = cryptoapis_client.generate_token_subscription(self, cryptocurrency_object.blockchain_id.blockchain_id, cryptocurrency_object.network_id.network_id, new_address.address)
                    
                elif cryptocurrency_object.type == "COIN":
                    new_subscription = cryptoapis_client.generate_coin_subscription(cryptocurrency_object.blockchain_id.blockchain_id, cryptocurrency_object.network_id.network_id, new_address.address)
            
            except:
                new_address.api_key = None
                new_address.status = "AVAILABLE"
                new_address.save()
                error = "Error generating address, please contact support"
                return None, error

            new_subscription_object = AddressSubscription.objects.create(
                subscription_id = new_subscription["referenceId"],
                event = new_subscription["eventType"],
                blockchain_id = cryptocurrency_object.blockchain_id,
                network_id = cryptocurrency_object.network_id,
                callback_url = new_subscription["callbackUrl"]
            )

            new_address.subscription_id = new_subscription_object
            new_address.save()

        return new_address, error

        # new_address.
        
        # #GENERATE TOKEN SUBSCRIPTION
        # if currency_object.blockchain == "ethereum" and currency_object.network == "mainnet":
        #     try:
        #         cryptoapis_client.generate_token_subscription(currency_object.blockchain, currency_object.network, deposit_address)
        #     except:
        #             newAddress.email = None
        #             newAddress.save()
        #             error = "Error generating address for ERC-20 Tokens, please contact support"
        #             return None, error
    
    def release_address(self, address_object):
        address_object.status = "AVAILABLE"
        address_object.api_key = None
        address_object.save()

        address_subscription = address_object.subscription_id

        if address_subscription is not None:
            try:
                cryptoapis_client = CryptoApis(network = address_subscription.network_id.network_id)
                cryptoapis_client.delete_blockchain_subscription(
                        address_subscription.blockchain_id.blockchain_id,
                        address_subscription.network_id.network_id,
                        address_subscription.subscription_id
                    )

                address_subscription.delete()
            except Exception as e:
                error = "Error releasing address. Please try again later."
                return error
        
        return None

    def generate_static_address(self, cryptocurrency_object, api_key_object, unique = False, type = "GENERIC_STATIC"):
        
        error = None
        
        if not unique:
            available_addresses = StaticAddress.objects.filter(
                address_id__cryptocurrency_id = cryptocurrency_object,
                address_id__api_key = api_key_object,
                type = type,
                status = "IN_USE"
            )

            if available_addresses.count() != 0:
                new_static_address = available_addresses.first()
                new_static_address.type = type
                new_static_address.save()
            else:
                unique = True
        
        if unique:
            cryptoapis_utils = CryptoApisUtils()
            address_object, error = cryptoapis_utils.generate_address(cryptocurrency_object, api_key_object)
            if error is not None:
                return None, error
            
            new_static_address = StaticAddress.objects.create(
                address_id = address_object,
                type = type,
                status = "IN_USE"
            )
        
        return new_static_address, error
    
    def release_static_address(self, static_address_object):
        dynamic_address_object = static_address_object.address_id

        error = self.release_address(dynamic_address_object)
        if error is not None:
            return error

        try:
            static_address_object.delete()
        except Exception as error:
            return error
        
        return None

    
    def withdraw_coin_transaction_funds(self, transaction_cryptocurrency, withdrawal_address, receiving_amount, source_address = None):
        cryptoapis_client = CryptoApis(network = transaction_cryptocurrency.network_id.network_id)

        try:
            if transaction_cryptocurrency.cryptoapis_type == "WALLET":
                transaction_response = cryptoapis_client.generate_coins_transaction_from_wallet(
                    transaction_cryptocurrency.blockchain_id.blockchain_id,
                    transaction_cryptocurrency.network_id.network_id,
                    withdrawal_address,
                    str(receiving_amount)
                )
            elif transaction_cryptocurrency.cryptoapis_type == "ADDRESS":

                if transaction_cryptocurrency.symbol == "TRX":
                    transaction_response = cryptoapis_client.generate_single_transaction_from_address_without_fee_priority(
                        transaction_cryptocurrency.blockchain_id.blockchain_id,
                        transaction_cryptocurrency.network_id.network_id,
                        source_address,
                        withdrawal_address,
                        str(receiving_amount)
                    )
                else:
                    transaction_response = cryptoapis_client.generate_coins_transaction_from_address(
                        transaction_cryptocurrency.blockchain_id.blockchain_id, 
                        transaction_cryptocurrency.network_id.network_id,
                        source_address, 
                        withdrawal_address, 
                        str(receiving_amount)
                    )
        except:
            error = "Error generating withdrawal"
            return error
        
        return None

    def withdraw_token_transaction_funds(self, source_address, transaction_cryptocurrency, withdrawal_address, receiving_amount):
        cryptoapis_client = CryptoApis(network = transaction_cryptocurrency.network_id.network_id)

        try:
            if transaction_cryptocurrency.type == "ERC-20":
                transaction_response = cryptoapis_client.generate_token_transaction_from_address(
                    transaction_cryptocurrency.blockchain_id.blockchain_id,
                    transaction_cryptocurrency.network_id.network_id,
                    source_address,
                    transaction_cryptocurrency.extra_data,
                    withdrawal_address,
                    str(receiving_amount)
                )
        except:
            error = "Error generating token withdrawal"
            return error

        return None             



def get_currencies_exchange_rate():
    cryptoapis_client = CryptoApis()

    exchange_rate_ltc = cryptoapis_client.get_exchange_rate_by_symbols("LTC", "USD")["rate"]
    rate_ltc = {
        "currency_name": "Litecoin",
        "symbol": "LTC",
        "exchange_rate": round(float(exchange_rate_ltc), 2)
    }

    exchange_rate_bch = cryptoapis_client.get_exchange_rate_by_symbols("BCH", "USD")["rate"]
    rate_bch = {
        "currency_name": "Bitcoin Cash",
        "symbol": "BCH",
        "exchange_rate": round(float(exchange_rate_bch), 2)
    }

    exchange_rate_dash = cryptoapis_client.get_exchange_rate_by_symbols("DASH", "USD")["rate"]
    rate_dash = {
        "currency_name": "Dash",
        "symbol": "DASH",
        "exchange_rate": round(float(exchange_rate_dash), 2)
    }

    exchange_rate_zec = cryptoapis_client.get_exchange_rate_by_symbols("ZEC", "USD")["rate"]
    rate_zec = {
        "currency_name": "Zcash",
        "symbol": "ZEC",
        "exchange_rate": round(float(exchange_rate_zec), 2)
    }

    exchange_rate_xrp = cryptoapis_client.get_exchange_rate_by_symbols("XRP", "USD")["rate"]
    rate_xrp = {
        "currency_name": "XRP",
        "symbol": "XRP",
        "exchange_rate": round(float(exchange_rate_xrp), 2)
    }

    exchange_rates = []
    exchange_rates.append(rate_ltc)
    exchange_rates.append(rate_bch)
    exchange_rates.append(rate_dash)
    exchange_rates.append(rate_zec)
    exchange_rates.append(rate_xrp)

    return exchange_rates

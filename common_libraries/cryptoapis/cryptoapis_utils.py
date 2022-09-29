# from atm_functions.models import Cryptocurrency, Address
from cryptocurrency.models import Address, Address_Subscription, Cryptocurrency

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
            cryptoapis_client = CryptoApis()

            number_of_addresses = Address.objects.filter(cryptocurrency_id = cryptocurrency_object).count()

            try:
                deposit_address = cryptoapis_client.generate_deposit_address(
                    cryptocurrency_object.blockchain_id.blockchain_id, 
                    cryptocurrency_object.network_id.network_id, 
                    number_of_addresses
                )
            except:
                error = "Error generating address. Please try again later."
                return None, error

            new_address = Address.objects.create(
                address_id = f"cryptosharepay|{cryptocurrency_object.blockchain_id.blockchain_id}|{cryptocurrency_object.network_id.network_id}|{number_of_addresses}",
                address = deposit_address,
                api_key = api_key_object,
                cryptocurrency_id = cryptocurrency_object,
                status = "IN_USE"
            )

            try:
                new_subscription = cryptoapis_client.generate_coin_subscription(cryptocurrency_object.blockchain_id.blockchain_id, cryptocurrency_object.network_id.network_id, deposit_address)
            except:
                new_address.api_key = None
                new_address.status = "AVAILABLE"
                new_address.save()
                error = "Error generating address, please contact support"
                return None, error
            
            print(new_subscription)
            #GENERATE COIN SUBSCRIPTION
            new_subscription_object = Address_Subscription.objects.create(
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

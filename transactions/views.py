from django.shortcuts import render
from django.contrib.auth.models import User
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from decimal import Decimal

from accounts.models import Account, Country
from businesses.models import Business
from api_keys.models import ApiKey
from cryptocurrency.models import Cryptocurrency, Blockchain, Network
from transactions.models import Transaction, TransactionBook, TransactionIns, TransactionOuts
from digital_currency.models import DigitalCurrency

# from rest_framework import Response
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.response  import Response
from rest_framework import status

from common_libraries.cryptoapis.cryptoapis_utils import CryptoApisUtils


class CreateTransaction(APIView):
    def post(self, request):
        data = request.data["data"]
        headers = request.headers

        #MISSING TO VERIFY ALL THIS INPUTS INTO MIDDLEWARE

        api_key = headers.get("X-API-Key", None)

        description = data["description"]
        digital_currency_code = data["digital_currency_code"]
        digital_currency_amount = data["digital_currency_amount"]
        cryptocurrency_code = data["cryptocurrency_code"]
        cryptocurrency_blockchain_id = data["cryptocurrency_blockchain_id"]
        customer_email = data.get("customer_email", None)
        customer_phone = data.get("customer_phone", None)

        CRYPTOCURRENCY_NETWORKS = {
            "TEST":{
                "BTC": "testnet",
                "BCH": "testnet",
                "LTC": "testnet",
                "DOGE": "testnet",
                "DASH": "testnet",
                "ETH": "goerli",
                "ETC": "mordor",
                "XRP": "testnet",
                "ZEC": "testnet",
                "TRX": "testnet",
            },
            "PRODUCTION": {
                "BTC": "mainnet",
                "BCH": "mainnet",
                "LTC": "mainnet",
                "DOGE": "mainnet",
                "DASH": "mainnet",
                "ETH": "mainnet",
                "ETC": "mainnet",
                "XRP": "mainnet",
                "ZEC": "mainnet",
                "TRX": "mainnet",
            }
        }

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

        cryptocurrency_object = Cryptocurrency.objects.filter(
            blockchain_id = blockchain_object,
            network_id = network_object,
            symbol = cryptocurrency_code
        )

        if not cryptocurrency_object.exists():
            return Response(
                str({
                "status": "ERROR",
                "message": "Invalid cryptocurrency_code"
                }), status=400)
        else:
            cryptocurrency_object = cryptocurrency_object.first()

        # print(cryptocurrency_object.__dict__)
        # GENERATE ADDRESS
        cryptoapis_utils = CryptoApisUtils()
        address_object, error = cryptoapis_utils.generate_address(cryptocurrency_object, api_key_object)
        if error is not None:
            return Response(
                {
                "status": "ERROR",
                "message": error
                }, status=400)

        """
        TRANSACTION TYPES

        - PAYMENT_REQUEST
        """

        digital_currency_amount_usd = Decimal(digital_currency_amount) / digital_currency_object.exchange_rate 

        cryptocurrency_amount = digital_currency_amount_usd / cryptocurrency_object.exchange_rate
        # cryptocurrency_amount = digital_currency_amount_usd / Decimal(41.44)

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



        return Response(
            {
                "status": "SUCCESS",
                "message": "Transaction created successfully",
                "data": {
                    "transaction_id": new_transaction.transaction_id,
                    "cryptocurrency_code": cryptocurrency_code,
                    "deposit_crypto_address": address_object.address,
                    "deposit_crypto_amount": cryptocurrency_amount,
                    "expiration_timestamp": new_transaction.expiration_datetime.timestamp(),
                    "creation_timestamp": new_transaction.creation_datetime.timestamp(),
                    "payment_url": "NOT_AVAILABLE"
                }
            }, status = 200)
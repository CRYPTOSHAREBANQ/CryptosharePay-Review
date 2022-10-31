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

from transactions.serializers import TransactionSerializer, TransactionsSerializer

# from rest_framework import Response
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.response  import Response
from rest_framework import status

from common_libraries.cryptoapis.cryptoapis_utils import CryptoApisUtils
from common_libraries.object_responses.object_responses import GenericCORSResponse
from common_libraries.constants.cryptocurrency import CRYPTOCURRENCY_NETWORKS
from common_libraries.transactions.transactions_utils import TransactionUtils
from common_libraries.emails.email_client import EmailClient


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
                return Response(
                {
                    "status": "ERROR",
                    "error": "Missing withdrawal address"
                }, status = 409)

        # print(cryptocurrency_object.__dict__)
        # GENERATE ADDRESS
        cryptoapis_utils = CryptoApisUtils()
        address_object, error = cryptoapis_utils.generate_address(cryptocurrency_object, api_key_object)
        if error is not None:
            return GenericCORSResponse(
                response = {
                    "status": "ERROR",
                    "message": error
                    },
                status = 400).get_response()


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
                "payment_url": "NOT_AVAILABLE"
            }
        }

        return GenericCORSResponse(
            response = response_object,
            status = 200
        ).get_response()

class GetTransactions(APIView):
    def get(self, request):
        headers = request.headers

        api_key = headers.get("X-API-Key", None)
        api_key_object = ApiKey.objects.get(api_key = api_key)

        transactions = Transaction.objects.filter(api_key = api_key_object)

        serializer = TransactionsSerializer(transactions, many=True)

        response_object = {
            "status": "SUCCESS",
            "message": "Transactions retrieved successfully",
            "data": {
                "transactions": serializer.data
            }
        }

        return GenericCORSResponse(
            response = response_object,
            status = 200
        ).get_response()

class GetTransaction(APIView):
    def get(self, request, transaction_id):
        headers = request.headers

        api_key = headers.get("X-API-Key", None)
        api_key_object = ApiKey.objects.get(api_key = api_key)

        transaction = Transaction.objects.get(api_key = api_key_object, transaction_id = transaction_id)

        # if not transaction.exists():
        #     return Response(
        #         {
        #         "status": "ERROR",
        #         "message": "Transaction not found"
        #         }, status=409)

        serializer = TransactionSerializer(transaction)

        response_object = {
            "status": "SUCCESS",
            "message": "Transaction retrieved successfully",
            "data": {
                "transaction": serializer.data
            }
        }

        return Response(response_object, status = 200)

class FilterTransactions(APIView):
    def get(self, request):
        headers = request.headers
        
        transaction_type = request.query_params.get("type", None).upper()
        
        api_key = headers.get("X-API-Key", None)
        api_key_object = ApiKey.objects.get(api_key = api_key)

        transactions = Transaction.objects.filter(api_key = api_key_object, type = transaction_type)

        serializer = TransactionsSerializer(transactions, many=True)

        response_object = {
            "status": "SUCCESS",
            "message": "Transactions retrieved successfully",
            "data": {
                "transactions": serializer.data
            }
        }

        return GenericCORSResponse(
            response = response_object,
            status = 200
        ).get_response()

class CancelTransaction(APIView):
    def post(self, request):
        headers = request.headers
        data = request.data["data"]

        api_key = headers.get("X-API-Key", None)
        api_key_object = ApiKey.objects.get(api_key = api_key)

        transaction_id = data["transaction_id"]
        
        transaction = Transaction.objects.get(api_key = api_key_object, transaction_id = transaction_id)

        transaction_address_object = transaction.address_id

        cryptoapis_utils = CryptoApisUtils()
        error = cryptoapis_utils.release_address(transaction_address_object)
        if error is not None:
            response_object = {
                "status": "ERROR",
                "message": error
            }

            #MISSING TO LOG ERROR
            return Response(response_object, status=503)

        transaction.state = "CANCELLED"
        transaction.status = "CANCELLED"
        transaction.save()

        email_client = EmailClient()
        email_client.cancel_transaction(transaction)

        response_object = {
            "status": "SUCCESS",
            "message": f"Transaction {transaction_id} cancelled successfully"
        }

        return Response(response_object, status=200)

class CompleteTransaction(APIView):
    def post(self, request):
        headers = request.headers
        data = request.data["data"]

        api_key = headers.get("X-API-Key", None)
        api_key_object = ApiKey.objects.get(api_key = api_key)

        transaction_id = data["transaction_id"]

        transaction = Transaction.objects.get(api_key = api_key_object, transaction_id = transaction_id)

        transaction_utils = TransactionUtils()
        error = transaction_utils.complete_transaction(transaction, api_key_object)
        if error is not None:
            response_object = {
                "status": "ERROR",
                "message": error
            }
            return Response(response_object, status=500)


        response_object = {
            "status": "SUCCESS",
            "message": f"Transaction {transaction_id} completed successfully"
        }

        return Response(response_object, status=200)



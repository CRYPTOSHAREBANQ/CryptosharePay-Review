from django.shortcuts import render
from django.contrib.auth.models import User
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

from accounts.models import Account, Country
from businesses.models import Business
from api_keys.models import ApiKey
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
from common_libraries.transactions.transactions_utils import TransactionUtils
from common_libraries.emails.email_client import EmailClient


class CreateTransactionDigitalToCrypto(APIView):
    def post(self, request):
        data = request.data["data"]
        headers = request.headers

        api_key = headers.get("X-API-Key", None)

        transaction_utils = TransactionUtils()
        response_object = transaction_utils.create_transaction_digital_to_crypto(api_key, data)
        if response_object["status"] == "ERROR":
            return Response(
                response_object, 
                status = 409
            )


        return Response(response_object, status=200)

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

        transaction_utils = TransactionUtils()
        error = transaction_utils.cancel_transaction(transaction)
        if error is not None:
            response_object = {
                "status": "ERROR",
                "message": error
            }
            return Response(response_object, status=503)

        email_client = EmailClient()
        email_client.cancel_transaction(transaction, str(transaction.api_key.user_id.email))

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



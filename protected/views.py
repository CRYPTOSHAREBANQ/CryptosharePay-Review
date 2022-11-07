from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth.models import User
from django.utils import timezone


from transactions.models import Transaction, TransactionBook ,TransactionIns
from cryptocurrency.models import Address, Blockchain, Cryptocurrency, Network

from accounts.models import Account
from api_keys.models import ApiKey

# from rest_framework import Response
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.response  import Response
from rest_framework import status

from transactions.serializers import TransactionSerializer, TransactionsSerializer
from common_libraries.emails.email_client import EmailClient
from common_libraries.transactions.transactions_utils import TransactionUtils

import json
import requests


class EmailHasAccount(APIView):
    def post(self, request):
        data = request.data["data"]
        user_object = None

        response_object = {
            "status": "SUCCESS",
            "message": "",
            "data": {
                "email_is_available": None,
                "type": None
            }
        }



        if User.objects.filter(email = data["email"]).exists():
            response_object["message"] = "Email already exists"
            response_object["data"]["email_is_available"] = False

            user_object = User.objects.get(email = data["email"])

            account_object = Account.objects.get(email = user_object)

            response_object["data"]["type"] = account_object.type
            
            status = 409

        else:
            response_object["message"] = "Email is available"
            response_object["data"]["email_is_available"] = True
            
            status = 200



        return Response(response_object, status=status)

class GetAPIKeyNoAccount(APIView):
    def get(self, request, type):
        headers = request.headers


        email = headers["X-Email"]

        if not User.objects.filter(email = email).exists():
            return Response(
                {
                "status": "ERROR",
                "message": "Invalid email"
                }, status=409)

        user = User.objects.get(email = email)

        account = Account.objects.filter(email = user, type = "NO_ACCOUNT")

        if not account.exists():
            return Response(
                {
                "status": "ERROR",
                "message": "Invalid email, user has an official account"
                }, status=409)

        account = account.first()
        

        if not ApiKey.objects.filter(user_id = account, type = type).exists():
            return Response(
                {
                "status": "ERROR",
                "message": "API Key does not exist"
                }, status=409)


        api_key_object = ApiKey.objects.get(
            user_id = account,
            type = type
        )

        response_object = {
            "status": "SUCCESS",
            "message": "API Key retrieved successfully",
            "data": {
                "api_key": api_key_object.api_key,
                "type": api_key_object.type
            }
        }
        
        return Response(response_object, status=200)

class GetTransaction(APIView):
    def get(self, request, transaction_id):
        headers = request.headers

        transaction = Transaction.objects.get(transaction_id = transaction_id)

        serializer = TransactionSerializer(transaction)

        response_object = {
            "status": "SUCCESS",
            "message": "Transaction retrieved successfully",
            "data": {
                "transaction": serializer.data
            }
        }

        return Response(response_object, status = 200)

class UpdateExchangeRates(APIView):
    def get(self, request):

        ids = []

        currencies = Cryptocurrency.objects.all()

        for currency in currencies:
            ids.append(currency.coingecko_name)

        url = f"https://api.coingecko.com/api/v3/simple/price?ids={','.join(ids)}&vs_currencies=usd&include_market_cap=false&include_24hr_vol=false&include_24hr_change=false&include_last_updated_at=false"
        # ids = 'ethereum,litecoin,bitcoin-cash,dash,zcash,usd-coin,tether,bitcoin,bitcoin,ripple,dogecoin'
        # url = f"https://api.coingecko.com/api/v3/simple/price?ids={ids}&vs_currencies=usd&include_market_cap=false&include_24hr_vol=false&include_24hr_change=false&include_last_updated_at=false"

        response = requests.get(url).json()

        for currency in currencies:
            
            try:
                coingecko_id = currency.coingecko_name

                exchange_rate = response[coingecko_id]["usd"]
                currency.exchange_rate = exchange_rate
                currency.save()
            except:
                print(f"{coingecko_id} not found in coingecko")
        

        return Response(status = 200)

        # to_delete_addresses = Address.objects.filter(expiration_datetime__date__lte=timezone.now().date())
class CancelExpiredTransactions(APIView):
    def get(self, request):

        to_cancel_transactions = Transaction.objects.filter(expiration_datetime__lte=timezone.now(), status = "PENDING")

        for transaction in to_cancel_transactions:

            transaction_utils = TransactionUtils()
            error = transaction_utils.expired_transaction(transaction)
            if error is not None:
                response_object = {
                    "status": "ERROR",
                    "message": error
                }
                return Response(response_object, status=503)

            email_client = EmailClient()
            email_client.cancel_expired_transaction(transaction, str(transaction.api_key.user_id.email))
        
        return Response(status = 200)
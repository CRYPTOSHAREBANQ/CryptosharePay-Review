from django.shortcuts import render
from django.contrib.auth.models import User
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from decimal import Decimal

from cryptocurrency.models import Cryptocurrency, Blockchain, Network
from assets.models import Asset
from transactions.models import TransactionOuts


# from rest_framework import Response
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.response  import Response
from rest_framework import status

from api_keys.models import ApiKey

from common_libraries.cryptoapis.cryptoapis_utils import CryptoApis
from common_libraries.transactions.transactions_utils import TransactionUtils


class CreateWithdrawal(APIView):
    def post(self, request):
        data = request.data["data"]
        headers = request.headers

        api_key = headers.get("X-API-Key", None)
        api_key_object = ApiKey.objects.get(api_key = api_key)

        cryptocurrency_code = data["cryptocurrency_code"].upper()
        cryptocurrency_blockchain_id = data["cryptocurrency_blockchain_id"]
        cryptocurrency_amount = data["cryptocurrency_amount"]
        withdrawal_address = data["withdrawal_address"]

        blockchain_object = Blockchain.objects.get(blockchain_id = cryptocurrency_blockchain_id)
        cryptocurrency_object = Cryptocurrency.objects.get(symbol = cryptocurrency_code, blockchain_id = blockchain_object)

        transaction_utils = TransactionUtils()
        error = transaction_utils.create_transaction_withdrawal(api_key_object, cryptocurrency_object, withdrawal_address, cryptocurrency_amount)
        if error is not None:
            if error == "Insufficient funds":
                code = 402
            elif error == "Withdrawals are not currently supported for this cryptocurrency":
                code = 409
            else:
                code = 503

            response_object = {
                "status": "ERROR",
                "message": error
            }
            return Response(response_object, status=code)

        #MISSING TO SEND EMAIL TO API KEY OWNER

        return Response(
            {
            "status": "SUCCESS",
            "message": "Withdrawal created successfully"
            }, status=200)
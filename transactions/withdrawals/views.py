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

from common_libraries.cryptoapis.cryptoapis_utils import CryptoApis

class CreateWithdrawal(APIView):
    def post(self, request):
        data = request.data["data"]
        headers = request.headers

        api_key = headers.get("X-API-Key", None)

        cryptocurrency_code = data["cryptocurrency_code"].upper()
        cryptocurrency_blockchain_id = data["cryptocurrency_blockchain_id"]
        cryptocurrency_amount = data["cryptocurrency_amount"]
        withdrawal_address = data["withdrawal_address"]

        wallet_currencies = {
                            "LTC": True,
                            "DASH": True,
                            "ZEC": True,
                            "BCH": True,
                            "BTC": True,
                            "DOGE": True
        }

        address_currencies = {
                            "XRP": True,
                            "ETH": True,
                            "USDC": True,
                            "USDT": True
        }


        cryptocurrency_object = Cryptocurrency.objects.get(symbol = cryptocurrency_code)
        blockchain_object = Blockchain.objects.get(blockchain_id = cryptocurrency_blockchain_id)

        asset = Asset.objects.get(
            api_key = api_key,
            cryptocurrency_id = cryptocurrency_object
        )

        if asset.amount < cryptocurrency_amount:
            return Response(
                {
                "status": "ERROR",
                "message": "Insufficient funds"
                }, status=400)

        cryptoapis_client = CryptoApis(network = cryptocurrency_object.network_id.network_id)

        if cryptocurrency_code in wallet_currencies:
            try:
                transaction_response = cryptoapis_client.generate_coins_transaction_from_wallet(
                    cryptocurrency_object.blockchain_id.blockchain_id,
                    cryptocurrency_object.network_id.network_id,
                    withdrawal_address,
                    cryptocurrency_amount
                )
            except:
                return Response(
                    {
                    "status": "ERROR",
                    "message": "Error generating withdrawal"
                    }, status=400)

        else:
            return Response(
                {
                "status": "ERROR",
                "message": "Withdrawals are not currently supported for this currency"
                }, status=400)
        
            # cryptoapis_client.generate_coins_transaction_from_address(
            #     cryptocurrency_object.blockchain_id.blockchain_id,
            #     cryptocurrency_object.network_id.network_id,
            #     sending_address,
            #     withdrawal_address,
            #     cryptocurrency_amount
            # )



        asset.amount -= Decimal(cryptocurrency_amount)
        asset.save()

        #MISSING TO SEND EMAIL TO API KEY OWNER

        return Response(
            {
            "status": "SUCCESS",
            "message": "Withdrawal created successfully"
            }, status=200)
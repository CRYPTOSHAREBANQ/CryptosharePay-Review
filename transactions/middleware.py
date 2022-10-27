from decimal import Decimal
from importlib.resources import path
from django.http import HttpResponse, Http404
from django.contrib import auth
from accounts.models import Account
from api_keys.models import ApiKey
from uuid import UUID

from cryptocurrency.models import Blockchain, Cryptocurrency, Network
from digital_currency.models import DigitalCurrency

from common_libraries.cryptoapis.cryptoapis import CryptoApis
from common_libraries.constants.cryptocurrency import CRYPTOCURRENCY_NETWORKS


import json

class TransactionVerification:
    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.
    
    def __call__(self, request):

        headers = request.META

        path_info = headers.get("PATH_INFO", None)        

        if "v1/transactions/" in path_info:
            try:
                data = json.loads(request.body.decode("utf-8"))
                data = data["data"]
            except:
                data = None

            if "create/" in path_info:

                description = data.get("description", None)
                digital_currency_code = data.get("digital_currency_code", None)
                digital_currency_amount = data.get("digital_currency_amount", None)
                cryptocurrency_code = data.get("cryptocurrency_code", None)
                cryptocurrency_blockchain_id = data.get("cryptocurrency_blockchain_id", None)
                withdrawal_address = data.get("withdrawal_address", None)

                if description:
                    if len(description) > 100:
                        return HttpResponse(
                            str({
                            "status": "ERROR",
                            "message": "Description max length is 100 characters"
                            }), status=409)

                if not digital_currency_code:
                    return HttpResponse(
                        str({
                        "status": "ERROR",
                        "message": "digital_currency_code not found"
                        }), status=409)
                else:
                    if not DigitalCurrency.objects.filter(digital_currency_id = digital_currency_code).exists():
                        return HttpResponse(
                            str({
                            "status": "ERROR",
                            "message": "Invalid digital_currency_code"
                            }), status=409)
                
                if not digital_currency_amount:
                    return HttpResponse(
                        str({
                        "status": "ERROR",
                        "message": "digital_currency_amount not found"
                        }), status=409)
                else:
                    try:
                        digital_currency_amount = Decimal(digital_currency_amount)
                    except ValueError:
                        return HttpResponse(
                            str({
                            "status": "ERROR",
                            "message": "Invalid digital_currency_amount"
                            }), status=409)

                if not cryptocurrency_code:
                    return HttpResponse(
                        str({
                        "status": "ERROR",
                        "message": "cryptocurrency_code not found"
                        }), status=409)
                else:
                    # Cryptocurrency.objects.get(
                    #     blockchain_id = blockchain_object,
                    #     network_id = network_object,
                    #     symbol = cryptocurrency_code
                    # )
                    if not Cryptocurrency.objects.filter(symbol = cryptocurrency_code).exists():
                        return HttpResponse(
                            str({
                            "status": "ERROR",
                            "message": "Invalid cryptocurrency_code"
                            }), status=409)

                if not cryptocurrency_blockchain_id:
                    return HttpResponse(
                        str({
                        "status": "ERROR",
                        "message": "cryptocurrency_blockchain_id not found"
                        }), status=409)
                else:
                    if not Blockchain.objects.filter(blockchain_id = cryptocurrency_blockchain_id).exists():
                        return HttpResponse(
                            str({
                            "status": "ERROR",
                            "message": "Invalid cryptocurrency_blockchain_id"
                            }), status=409)

                if withdrawal_address:
                    api_key = headers.get("HTTP_X_API_KEY", None)
                    api_key_object = ApiKey.objects.get(api_key = api_key)

                    network_object = Network.objects.get(network_id = CRYPTOCURRENCY_NETWORKS[api_key_object.type][cryptocurrency_code])
                    cryptoapis_client = CryptoApis(network = network_object.network_id)

                    if not cryptoapis_client.validate_address(cryptocurrency_blockchain_id, network_object.network_id, withdrawal_address):
                        return HttpResponse(
                            str({
                            "status": "ERROR",
                            "message": "Invalid withdrawal_address"
                            }), status=409)

        response = self.get_response(request)

        return response
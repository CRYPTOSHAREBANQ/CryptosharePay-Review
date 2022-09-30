from decimal import Decimal
from importlib.resources import path
from django.http import HttpResponse, Http404
from django.contrib import auth
from accounts.models import Account
from api_keys.models import Api_Key
from uuid import UUID

from cryptocurrency.models import Blockchain, Cryptocurrency
from digital_currency.models import Digital_Currency

import json

class Transaction_Verification:
    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.
    
    def __call__(self, request):

        headers = request.META

        path_info = headers.get("PATH_INFO", None)

        try:
            data = json.loads(request.body.decode("utf-8"))
            data = data["data"]
        except:
            data = None
        

        if "v1/transactions/" in path_info:

            if "create-transaction/" in path_info:

                description = data.get("description", None)
                digital_currency_code = data.get("digital_currency_code", None)
                digital_currency_amount = data.get("digital_currency_amount", None)
                cryptocurrency_code = data.get("cryptocurrency_code", None)
                cryptocurrency_blockchain = data.get("cryptocurrency_blockchain", None)

                if description:
                    if len(description) > 100:
                        return HttpResponse(
                            str({
                            "status": "ERROR",
                            "message": "Description max length is 100 characters"
                            }), status=400)

                if not digital_currency_code:
                    return HttpResponse(
                        str({
                        "status": "ERROR",
                        "message": "digital_currency_code not found"
                        }), status=400)
                else:
                    if not Digital_Currency.objects.filter(digital_currency_id = digital_currency_code).exists():
                        return HttpResponse(
                            str({
                            "status": "ERROR",
                            "message": "Invalid digital_currency_code"
                            }), status=400)
                
                if not digital_currency_amount:
                    return HttpResponse(
                        str({
                        "status": "ERROR",
                        "message": "digital_currency_amount not found"
                        }), status=400)
                else:
                    try:
                        digital_currency_amount = Decimal(digital_currency_amount)
                    except ValueError:
                        return HttpResponse(
                            str({
                            "status": "ERROR",
                            "message": "Invalid digital_currency_amount"
                            }), status=400)

                if not cryptocurrency_code:
                    return HttpResponse(
                        str({
                        "status": "ERROR",
                        "message": "cryptocurrency_code not found"
                        }), status=400)
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
                            }), status=400)

                if not cryptocurrency_blockchain:
                    return HttpResponse(
                        str({
                        "status": "ERROR",
                        "message": "cryptocurrency_blockchain not found"
                        }), status=400)
                else:
                    if not Blockchain.objects.filter(blockchain_id = cryptocurrency_blockchain).exists():
                        return HttpResponse(
                            str({
                            "status": "ERROR",
                            "message": "Invalid cryptocurrency_blockchain"
                            }), status=400)




        response = self.get_response(request)

        return response
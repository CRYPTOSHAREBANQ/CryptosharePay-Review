from decimal import Decimal
from importlib.resources import path
from django.http import HttpResponse, Http404
from django.contrib import auth
from accounts.models import Account
from api_keys.models import ApiKey
from uuid import UUID

import json

from digital_currency.models import DigitalCurrency

class DigitalCurrencyVerification:
    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.

    def __call__(self, request):
        # response = self.get_response(request)

        # Code to be executed for each request/response after
        # the view is called.
        headers = request.META

        path_info = headers.get("PATH_INFO", None)


        if "v1/digital-currency/" in path_info:

            if "get-digital-currency/" in path_info:

                # GET URL PARAMETERS FROM URL PATH
                # ['v1', 'digital-currency', 'get-digital-currency', 'DIGITAL_CURRENCY_CODE']
                url_path = path_info.split("/")[1:-1]
                # print(path_info)
                
                digital_currency_code = url_path[3]

                if not digital_currency_code or not DigitalCurrency.objects.filter(digital_currency_id = digital_currency_code).exists():
                    return HttpResponse(
                        str({
                        "status": "ERROR",
                        "message": "Digital currency not found"
                        }), status=400)

            pass
        

        ### DO NOT REMOVE ###
        ### DO NOT REMOVE ###
        ### DO NOT REMOVE ###

        response = self.get_response(request)

        return response

        ### DO NOT REMOVE ###
        ### DO NOT REMOVE ###
        ### DO NOT REMOVE ###
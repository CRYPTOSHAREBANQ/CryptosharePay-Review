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
            pass
        

        ### DO NOT REMOVE ###
        ### DO NOT REMOVE ###
        ### DO NOT REMOVE ###

        response = self.get_response(request)

        return response

        ### DO NOT REMOVE ###
        ### DO NOT REMOVE ###
        ### DO NOT REMOVE ###
    
    def process_view(self, request, view_func, view_args, view_kwargs):
        headers = request.META

        path_info = headers.get("PATH_INFO", None)

        if "v1/digital-currency/" in path_info:
            if "digital_currency_code" in view_kwargs.keys():
                digital_currency_code = view_kwargs["digital_currency_code"]

                if not digital_currency_code or not DigitalCurrency.objects.filter(digital_currency_id = digital_currency_code).exists():
                    return HttpResponse(
                        str({
                        "status": "ERROR",
                        "message": "Digital currency not found"
                        }), status=409)
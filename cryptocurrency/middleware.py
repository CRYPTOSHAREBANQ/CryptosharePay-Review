from decimal import Decimal
from importlib.resources import path
from django.http import HttpResponse, Http404
from django.contrib import auth
from accounts.models import Account
from api_keys.models import ApiKey
from uuid import UUID

import json

from cryptocurrency.models import Cryptocurrency


class CryptocurrencyVerification:
    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.

    def __call__(self, request):
        # response = self.get_response(request)

        # Code to be executed for each request/response after
        # the view is called.
        headers = request.META

        path_info = headers.get("PATH_INFO", None)


        if "v1/cryptocurrency/" in path_info:

            if "get-cryptocurrency/" in path_info:

                print(request.session["url_vars"])

                # cryptocurrency_code = request.session["url_vars"]["code"]
                cryptocurrency_code = None

                if not cryptocurrency_code or Cryptocurrency.objects.filter(cryptocurrency_code = cryptocurrency_code).exists():
                    return HttpResponse(
                        str({
                        "status": "ERROR",
                        "message": "Cryptocurrency code not found"
                        }), status=400)


            # api_key = data.get("api_key", None)

            # if not api_key or not ApiKey.objects.filter(api_key = api_key, user_id = account_object).exists():
            #     return HttpResponse(
            #         str({
            #         "status": "ERROR",
            #         "message": "Invalid API Key"
            #         }), status=400)
            pass
        

        ### DO NOT REMOVE ###
        ### DO NOT REMOVE ###
        ### DO NOT REMOVE ###

        response = self.get_response(request)

        return response

        ### DO NOT REMOVE ###
        ### DO NOT REMOVE ###
        ### DO NOT REMOVE ###
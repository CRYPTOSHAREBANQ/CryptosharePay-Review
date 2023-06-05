from decimal import Decimal
from importlib.resources import path
from django.http import HttpResponse, Http404
from django.contrib import auth
from accounts.models import Account
from api_keys.models import ApiKey
from uuid import UUID

import json

from cryptocurrency.models import Cryptocurrency, Network

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

                # GET URL PARAMETERS FROM URL PATH
                # ['v1', 'cryptocurrency', 'get-cryptocurrency', 'CRYPTOCURRENCY_CODE', 'CRYPTOCURRENCY_NETWORK']
                url_path = path_info.split("/")[1:-1]
                # print(path_info)
                
                cryptocurrency_code = url_path[3]
                network = url_path[4]

                print(cryptocurrency_code)
                if not cryptocurrency_code or not Cryptocurrency.objects.filter(symbol = cryptocurrency_code, network_id__network_id = network).exists():
                    return HttpResponse(
                        str({
                        "status": "ERROR",
                        "message": "Cryptocurrency not found"
                        }), status=409)

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

        if "v1/cryptocurrency/" in path_info:
            if "cryptocurrency_code" in view_kwargs.keys():
                cryptocurrency_code = view_kwargs["cryptocurrency_code"]

                if not cryptocurrency_code or not Cryptocurrency.objects.filter(symbol = cryptocurrency_code).exists():
                    return HttpResponse(
                        str({
                        "status": "ERROR",
                        "message": "Cryptocurrency code not found"
                        }), status=409)
                
            if "network" in view_kwargs.keys():
                network = view_kwargs["network"]

                if not network or not Network.objects.filter(network_id = network).exists():
                    return HttpResponse(
                        str({
                        "status": "ERROR",
                        "message": "Cryptocurrency network not found"
                        }), status=409)
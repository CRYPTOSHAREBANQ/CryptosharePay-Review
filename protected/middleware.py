from decimal import Decimal
from importlib.resources import path
from django.http import HttpResponse, Http404
from django.contrib import auth

from uuid import UUID

import json

from cryptocurrency.models import Cryptocurrency
from transactions.models import Transaction
from accounts.models import Account
from api_keys.models import ApiKey

class ProtectedVerification:
    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.

    def __call__(self, request):
        # response = self.get_response(request)

        # Code to be executed for each request/response after
        # the view is called.
        headers = request.META

        path_info = headers.get("PATH_INFO", None)


        if "protected/" in path_info:

            if "accounts/email-has-account/" in path_info:
                pass

            elif "api-keys/api-key-no-account/" in path_info:
                pass
            
            elif "transactions/payments/" in path_info:
                pass

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

        if "v1/protected/transactions" in path_info:

            if "payments/" in path_info:

                if "transaction_id" in view_kwargs.keys():
                    transaction_id = view_kwargs["transaction_id"]

                    try:
                        uuid_obj = UUID(transaction_id, version=4)
                    except ValueError:
                        return HttpResponse(
                            str({
                            "status": "ERROR",
                            "message": "Invalid transaction_id"
                            }), status=409)

                    api_key = headers.get("HTTP_X_API_KEY", None)
                    api_key_object = ApiKey.objects.get(api_key = api_key)

                    if not transaction_id or not Transaction.objects.filter(api_key = api_key_object, transaction_id = transaction_id).exists():
                        return HttpResponse(
                            str({
                            "status": "ERROR",
                            "message": "Transaction not found"
                            }), status=409)
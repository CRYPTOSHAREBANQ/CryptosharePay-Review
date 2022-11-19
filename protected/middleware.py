from decimal import Decimal
from importlib.resources import path
from django.http import HttpResponse, Http404
from django.contrib import auth
from django.contrib.auth.models import User

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
            
            if "accounts/" in path_info:
                if "email-has-account/" in path_info:
                    pass
                
                elif "request-login-dashboard" in path_info:
                    email = headers.get("HTTP_X_EMAIL", None)

                    if not email:
                        return HttpResponse(
                            str({
                            "status": "ERROR",
                            "message": "Invalid email"
                            }), status=400)

                    #VERIFY CREDENTIALS
                    user_object = User.objects.filter(email = email)

                    if not user_object:
                        return HttpResponse(
                            str({
                            "status": "ERROR",
                            "message": "Invalid credentials"
                            }), status=401)

                elif "login-dashboard/" in path_info:
                    email = headers.get("HTTP_X_EMAIL", None)
                    security_password = headers.get("HTTP_X_SECURITY_PASSWORD", None)
                    # security_pin = headers.get("HTTP_X_SECURITY_PIN", None)

                    if not email or not security_password:
                        return HttpResponse(
                            str({
                            "status": "ERROR",
                            "message": "Invalid email or password"
                            }), status=400)

                    #VERIFY CREDENTIALS
                    user_object = User.objects.filter(email = email)

                    if not user_object:
                        return HttpResponse(
                            str({
                            "status": "ERROR",
                            "message": "Invalid credentials"
                            }), status=401)
                    else:
                        user_object = user_object.first()

                    account_object = Account.objects.get(email = user_object)
            
                    if account_object.random_password is None:
                        return HttpResponse(
                            str({
                            "status": "ERROR",
                            "message": "Login not requested"
                            }), status=409)

                    if not security_password or account_object.random_password != security_password:
                        return HttpResponse(
                            str({
                            "status": "ERROR",
                            "message": "Invalid security password"
                            }), status=401)

            elif "api-keys/api-key-no-account/" in path_info:
                email = headers.get("HTTP_X_EMAIL", None)

                if not email:
                    return HttpResponse(
                        str({
                        "status": "ERROR",
                        "message": "Missing email header"
                        }), status=409)

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

                    if not transaction_id or not Transaction.objects.filter(transaction_id = transaction_id).exists():
                        return HttpResponse(
                            str({
                            "status": "ERROR",
                            "message": "Transaction not found"
                            }), status=409)
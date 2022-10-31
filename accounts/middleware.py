from decimal import Decimal
from importlib.resources import path
from django.contrib.auth.models import User
from django.http import HttpResponse, Http404
from django.contrib import auth

from accounts.models import Account, Country
from businesses.models import Business
from api_keys.models import ApiKey

from common_libraries.constants.accounts import ACCOUNT_TYPES, NO_ACCOUNT_REDIRECT_URL
from uuid import UUID

import json

from digital_currency.models import DigitalCurrency

class AccountVerification:
    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.

    def __call__(self, request):
        # response = self.get_response(request)

        # Code to be executed for each request/response after
        # the view is called.
        headers = request.META

        path_info = headers.get("PATH_INFO", None)


        if "v1/accounts/" in path_info:

            # GET REQUEST BODY
            try:
                data = json.loads(request.body.decode("utf-8"))
                data = data["data"]
            except:
                data = None

            if "create/" in path_info:

                # api_key_type = data.get("type", None)
                customer_info = data.get("customer_info", None)
                business_info = data.get("business_info", None)

                if not customer_info:
                    return HttpResponse(
                        str({
                        "status": "ERROR",
                        "message": "Invalid customer_info"
                        }), status=409)

                if not "country_id" in customer_info or not Country.objects.filter(country_id = customer_info["country_id"]).exists():
                    return HttpResponse(
                        str({
                        "status": "ERROR",
                        "message": "Invalid country_id does not exist"
                        }), status=409)

                if Country.objects.get(country_id = customer_info["country_id"]).status == "BLOCK":
                    return HttpResponse(
                        str({
                        "status": "ERROR",
                        "message": F"Your country doesnt need to create an account, please go to: {NO_ACCOUNT_REDIRECT_URL}, or go to CryptosharePay Site -> Payments"
                        }), status=409)

                if User.objects.filter(email = customer_info["email"]).exists():
                    return HttpResponse(
                        str({
                        "status": "ERROR",
                        "message": "Email already exists"
                        }), status=409)
                
                if customer_info["password"] != customer_info["confirm_password"]:
                    return HttpResponse(
                        str({
                        "status": "ERROR",
                        "message": "Passwords do not match"
                        }), status=409)       
                
                if customer_info["type"] not in ACCOUNT_TYPES:
                    return HttpResponse(
                        str({
                        "status": "ERROR",
                        "message": "Invalid type"
                        }), status=409)

                if business_info:
                    if not "description" in business_info or len(business_info["description"]) > 32:
                        return HttpResponse(
                            str({
                            "status": "ERROR",
                            "message": "Invalid description"
                            }), status=409)

        ### DO NOT REMOVE ###
        ### DO NOT REMOVE ###
        ### DO NOT REMOVE ###

        response = self.get_response(request)

        return response

        ### DO NOT REMOVE ###
        ### DO NOT REMOVE ###
        ### DO NOT REMOVE ###
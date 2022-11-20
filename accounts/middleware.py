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
                        }), status=400)

                if not "country_id" in customer_info or not Country.objects.filter(country_id = customer_info["country_id"]).exists():
                    return HttpResponse(
                        str({
                        "status": "ERROR",
                        "message": "Invalid country_id does not exist"
                        }), status=400)

                if Country.objects.get(country_id = customer_info["country_id"]).status == "BLOCK":
                    return HttpResponse(
                        str({
                        "status": "ERROR",
                        "message": F"Your country doesnt need to create an account, please go to: {NO_ACCOUNT_REDIRECT_URL}, or go to CryptosharePay Site -> Payments"
                        }), status=400)

                if User.objects.filter(email = customer_info["email"].lower()).exists():
                    return HttpResponse(
                        str({
                        "status": "ERROR",
                        "message": "Email already exists"
                        }), status=400)
                
                if customer_info["password"] != customer_info["confirm_password"]:
                    return HttpResponse(
                        str({
                        "status": "ERROR",
                        "message": "Passwords do not match"
                        }), status=400)       
                
                if customer_info["type"] not in ACCOUNT_TYPES:
                    return HttpResponse(
                        str({
                        "status": "ERROR",
                        "message": "Invalid type"
                        }), status=400)

                if business_info:
                    if not "description" in business_info or len(business_info["description"]) > 32:
                        return HttpResponse(
                            str({
                            "status": "ERROR",
                            "message": "Invalid description"
                            }), status=400)
        
            elif "account-info/" in path_info:
                email = headers.get("HTTP_X_EMAIL", None)
                password = headers.get("HTTP_X_PASSWORD", None)

                ### <------ CREDENTIALS VERIFICATION ------> ###
                ### <------ CREDENTIALS VERIFICATION ------> ###

                #VERIFY CREDENTIALS
                if not email or not password:
                    return HttpResponse(
                        str({
                        "status": "ERROR",
                        "message": "Email or Password not found"
                        }), status=400)

                user_object = auth.authenticate(
                    username = email,
                    password = password
                )

                if not user_object:
                    return HttpResponse(
                        str({
                        "status": "ERROR",
                        "message": "Invalid credentials"
                        }), status=401)
                
                ### <------ CREDENTIALS VERIFICATION ------> ###
                ### <------ CREDENTIALS VERIFICATION ------> ###

                pass

            elif "request-customer-id/" in path_info:
                email = headers.get("HTTP_X_EMAIL", None)
                password = headers.get("HTTP_X_PASSWORD", None)

                if not email or not password:
                    return HttpResponse(
                        str({
                        "status": "ERROR",
                        "message": "Invalid email or password"
                        }), status=400)

                #VERIFY CREDENTIALS
                user_object = auth.authenticate(
                    username = email,
                    password = password
                )

                if not user_object:
                    return HttpResponse(
                        str({
                        "status": "ERROR",
                        "message": "Invalid credentials"
                        }), status=401)

            elif "account-customer-id" in path_info:
                email = headers.get("HTTP_X_EMAIL", None)
                password = headers.get("HTTP_X_PASSWORD", None)
                security_pin = headers.get("HTTP_X_SECURITY_PIN", None)

                if not email or not password:
                    return HttpResponse(
                        str({
                        "status": "ERROR",
                        "message": "Invalid email or password"
                        }), status=400)

                #VERIFY CREDENTIALS
                user_object = auth.authenticate(
                    username = email,
                    password = password
                )

                if not user_object:
                    return HttpResponse(
                        str({
                        "status": "ERROR",
                        "message": "Invalid credentials"
                        }), status=401)

                account_object = Account.objects.get(email = user_object)
        
                if account_object.security_pin is None:
                    return HttpResponse(
                        str({
                        "status": "ERROR",
                        "message": "Customer ID not requested"
                        }), status=409)

                if not security_pin or account_object.security_pin != security_pin:
                    return HttpResponse(
                        str({
                        "status": "ERROR",
                        "message": "Invalid security pin"
                        }), status=401)

        elif "v1/api-keys/" in path_info:
            customer_id = headers.get("HTTP_X_CUSTOMER_ID", None)
            email = headers.get("HTTP_X_EMAIL", None)
            password = headers.get("HTTP_X_PASSWORD", None)

            if not email:
                return HttpResponse(
                    str({
                    "status": "ERROR",
                    "message": "X-Email not found"
                    }), status=400)

            ### <------ X-CUSTOMER-ID VERIFICATION ------> ###
            ### <------ X-CUSTOMER-ID VERIFICATION ------> ###

            #VERIFY X-CUSTOMER-ID HEADER IS NOT EMPTY
            if not customer_id:
                return HttpResponse(
                    str({
                    "status": "ERROR",
                    "message": "X-Customer-Id not found"
                    }), status=400)

            #VERIFY X-CUSTOMER-ID FORMAT
            try:
                uuid_obj = UUID(customer_id, version=4)
            except ValueError:
                return HttpResponse(
                    str({
                    "status": "ERROR",
                    "message": "Invalid X-Customer-Id"
                    }), status=400)

            #VERIFY X-CUSTOMER-ID ACCOUNT EXISTS
            if not Account.objects.filter(user_id = customer_id).exists():
                return HttpResponse(
                    str({
                    "status": "ERROR",
                    "message": "Invalid X-Customer-Id"
                    }), status=400)
                                
            ### <------ X-CUSTOMER-ID VERIFICATION ------> ###
            ### <------ X-CUSTOMER-ID VERIFICATION ------> ###

            ### <------ CREDENTIALS VERIFICATION ------> ###
            ### <------ CREDENTIALS VERIFICATION ------> ###

            if "get-by-business-id/" not in path_info:
                #VERIFY CREDENTIALS
                if not email or not password:
                    return HttpResponse(
                        str({
                        "status": "ERROR",
                        "message": "Email or Password not found"
                        }), status=400)

                user_object = auth.authenticate(
                    username = email,
                    password = password
                )

                if not user_object:
                    return HttpResponse(
                        str({
                        "status": "ERROR",
                        "message": "Invalid credentials"
                        }), status=401)
            
            ### <------ CREDENTIALS VERIFICATION ------> ###
            ### <------ CREDENTIALS VERIFICATION ------> ###
            

        ### DO NOT REMOVE ###
        ### DO NOT REMOVE ###
        ### DO NOT REMOVE ###

        response = self.get_response(request)

        return response

        ### DO NOT REMOVE ###
        ### DO NOT REMOVE ###
        ### DO NOT REMOVE ###
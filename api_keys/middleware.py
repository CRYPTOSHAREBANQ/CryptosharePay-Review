from decimal import Decimal
from django.http import HttpResponse, Http404
from django.contrib.auth.models import User
from django.contrib import auth
from accounts.models import Account
from api_keys.models import ApiKey
from uuid import UUID

import json

class APIKeyVerification:
    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.

    def __call__(self, request):
        # response = self.get_response(request)

        # Code to be executed for each request/response after
        # the view is called.
            
        headers = request.META
    
        path_info = headers.get("PATH_INFO", None)

        # GET REQUEST BODY
        try:
            data = json.loads(request.body.decode("utf-8"))
            data = data["data"]
        except:
            data = None

        ### API KEYS ###
        ### API KEYS ###
        ### API KEYS ###

        if "v1/accounts/" in path_info:            
            pass
        
        elif "v1/api-keys/" in path_info:

            ### <------ ENDPOINTS ------> ###
            ### <------ ENDPOINTS ------> ###

            if "create/" in path_info:

                email = headers.get("HTTP_X_EMAIL", None)

                #VERIFY API-KEY TYPE
                API_KEY_TYPES = {"TEST", "PRODUCTION"}

                user_object = User.objects.get(email = email)
                account_object = Account.objects.get(email = user_object)

                api_key_type = data.get("type", None)
                if not api_key_type in API_KEY_TYPES:
                    return HttpResponse(
                        str({
                        "status": "ERROR",
                        "message": "Invalid API Key type"
                        }), status=400)

                #VERIFY IF USER ALREADY HAS API KEY
                if ApiKey.objects.filter(user_id = account_object, type = api_key_type).exists():
                    return HttpResponse(
                        str({
                        "status": "ERROR",
                        "message": "User already has an API Key"
                        }), status=403)

                #VERIFY BUSINESS_ID FORMAT
                business_id = data.get("business_id", None)
                if business_id:
                    try:
                        uuid_obj = UUID(business_id, version=4)
                    except ValueError:
                        return HttpResponse(
                            str({
                            "status": "ERROR",
                            "message": "Invalid business_id"
                            }), status=400)

            elif "all/" in path_info:
                pass
                
            else:
                api_key = data.get("api_key", None)

                if not api_key or not ApiKey.objects.filter(api_key = api_key, user_id = account_object).exists():
                    return HttpResponse(
                        str({
                        "status": "ERROR",
                        "message": "Invalid API Key"
                        }), status=401)

            ### <------ ENDPOINTS ------> ###
            ### <------ ENDPOINTS ------> ###
        elif "v1/protected" in path_info:
            pass
        else:
            allowed_endpoints = ["/ping/", "/cryptoapisverifydomain/", "/webhooks/cryptoapis/subscriptions/ConfirmedCoinTransactions/"]
            if path_info not in allowed_endpoints:
                api_key = headers.get("HTTP_X_API_KEY", None)
                api_key_verification = self.verify_api_key(api_key)
                if api_key_verification:
                    return api_key_verification

        ### DO NOT REMOVE ###
        ### DO NOT REMOVE ###
        ### DO NOT REMOVE ###

        response = self.get_response(request)

        return response

        ### DO NOT REMOVE ###
        ### DO NOT REMOVE ###
        ### DO NOT REMOVE ###

    def verify_api_key(self, api_key):
        if not api_key or not ApiKey.objects.filter(api_key = api_key).exists():
            return HttpResponse(
                str({
                "status": "ERROR",
                "message": "Invalid API Key"
                }), status=401)
        else:
            return None
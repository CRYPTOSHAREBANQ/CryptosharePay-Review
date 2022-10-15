from decimal import Decimal
from django.http import HttpResponse, Http404
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
        if "v1/api-keys/" in path_info:
            customer_id = headers.get("HTTP_X_CUSTOMER_ID", None)
            email = headers.get("HTTP_X_EMAIL", None)
            password = headers.get("HTTP_X_PASSWORD", None)

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
                    }), status=400)
            
            account_object = Account.objects.get(email = user_object)

            ### <------ CREDENTIALS VERIFICATION ------> ###
            ### <------ CREDENTIALS VERIFICATION ------> ###


            ### <------ ENDPOINTS ------> ###
            ### <------ ENDPOINTS ------> ###

            if "create/" in path_info:

                #VERIFY API-KEY TYPE
                API_KEY_TYPES = {"TEST", "PRODUCTION"}

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
                        }), status=400)

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

            if "all/" in path_info:
                pass
                
            else:
                api_key = data.get("api_key", None)

                if not api_key or not ApiKey.objects.filter(api_key = api_key, user_id = account_object).exists():
                    return HttpResponse(
                        str({
                        "status": "ERROR",
                        "message": "Invalid API Key"
                        }), status=400)

            ### <------ ENDPOINTS ------> ###
            ### <------ ENDPOINTS ------> ###

        elif "v1/accounts/" in path_info:            
            pass
        
        # elif "v1/businesses/" in path_info:
        #     api_key = headers.get("HTTP_X_API_KEY", None)
        #     api_key_verification = self.verify_api_key(api_key)
        #     if api_key_verification:
        #         return api_key_verification
        #     pass

        # elif "v1/cryptocurrency/" in path_info:
        #     api_key = headers.get("HTTP_X_API_KEY", None)
        #     api_key_verification = self.verify_api_key(api_key)
        #     if api_key_verification:
        #         return api_key_verification
        #     pass
        
        # elif "v1/digital-currency/" in path_info:
        #     api_key = headers.get("HTTP_X_API_KEY", None)
        #     api_key_verification = self.verify_api_key(api_key)
        #     if api_key_verification:
        #         return api_key_verification
        #     pass

        # elif "v1/transactions/" in path_info:
        #     api_key = headers.get("HTTP_X_API_KEY", None)
        #     api_key_verification = self.verify_api_key(api_key)
        #     if api_key_verification:
        #         return api_key_verification

        else:
            print(path_info)
            if not "ping/" in path_info and not "cryptoapisverifydomain/" in path_info:
                api_key = headers.get("HTTP_X_API_KEY", None)
                api_key_verification = self.verify_api_key(api_key)
                if api_key_verification:
                    return api_key_verification
            # print(path_info)        

        # print(headers)

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
                }), status=400)
        else:
            return None
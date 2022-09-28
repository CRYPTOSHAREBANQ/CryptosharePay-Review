from importlib.resources import path
from django.http import HttpResponse, Http404
from django.contrib import auth
from accounts.models import Account
from uuid import UUID

import json

class API_Key_Verification:
    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.

    def __call__(self, request):
        # response = self.get_response(request)

        # Code to be executed for each request/response after
        # the view is called.
        
        try:
            data = json.loads(request.body.decode("utf-8"))
            data = data["data"]
        except:
            print("EMPTY BODY")
            
        headers = request.META

        path_info = headers.get("PATH_INFO", None)

        ### API KEYS ###
        ### API KEYS ###
        ### API KEYS ###
        if "v1/api_keys/" in path_info:
            customer_id = headers.get("HTTP_X_CUSTOMER_ID", None)
            email = headers.get("HTTP_X_EMAIL", None)
            password = headers.get("HTTP_X_PASSWORD", None)



            if not customer_id:
                return HttpResponse(
                    str({
                    "status": "ERROR",
                    "message": "X-Customer-Id not found"
                    }), status=400)

            try:
                uuid_obj = UUID(customer_id, version=4)
            except ValueError:
                return HttpResponse(
                    str({
                    "status": "ERROR",
                    "message": "Invalid X-Customer-Id"
                    }), status=400)

            if not Account.objects.filter(user_id = customer_id).exists():
                return HttpResponse(
                    str({
                    "status": "ERROR",
                    "message": "Invalid X-Customer-Id"
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

            # if "get_api_keys/" in path_info:

                

                
                

            


        # print(headers)
        response = self.get_response(request)

        return response
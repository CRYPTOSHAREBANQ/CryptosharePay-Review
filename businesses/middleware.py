from decimal import Decimal
from django.http import HttpResponse, Http404
from django.contrib.auth.models import User
from django.contrib import auth

from accounts.models import Account
from api_keys.models import ApiKey
from businesses.models import Business

from uuid import UUID

import json

class BusinessVerification:
    def __init__(self, get_response) -> None:
        self.get_response = get_response
    
    def __call__(self, request):
        headers = request.META

        path_info = headers.get("PATH_INFO", None)

        if "v1/accounts/" in path_info:
            pass
        
        elif "v1/api-keys/" in path_info:
            if "get-by-business-id/" in path_info:
                customer_id = headers.get("HTTP_X_CUSTOMER_ID", None)
                business_id = headers.get("HTTP_X_BUSINESS_ID", None)
                
                account_object = Account.objects.get(user_id = customer_id)

                #VERIFY BUSINESS_ID FORMAT
                try:
                    uuid_obj = UUID(business_id, version=4)
                except ValueError:
                    return HttpResponse(
                        str({
                        "status": "ERROR",
                        "message": "Invalid business_id"
                        }), status=400)
                
                #VERIFY BUSINESS_ID
                if not Business.objects.filter(business_id = business_id, user_id = account_object).exists():
                    return HttpResponse(
                        str({
                        "status": "ERROR",
                        "message": "Invalid business_id"
                        }), status=400)

        ### DO NOT REMOVE ###
        ### DO NOT REMOVE ###
        ### DO NOT REMOVE ###

        response = self.get_response(request)

        return response

        ### DO NOT REMOVE ###
        ### DO NOT REMOVE ###
        ### DO NOT REMOVE ###
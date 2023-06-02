from django.shortcuts import render
from django.contrib import auth
from django.contrib.auth.models import User

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response  import Response
from rest_framework import status

from api_keys.models import ApiKey , ApiKey_individual
from accounts.models import Account,Insividual_Account
from businesses.models import Business

from api_keys.serializers import ApiKeysSerializer

import secrets

class CreateApiKey(APIView):
    def post(self, request):
        data = request.data["data"]
        headers = request.headers

        customer_id = headers.get("X-Customer-Id", None)
        business_id = data.get("business_id", None)
        api_key_type = data.get("type", None)

        # business_object = None
        if Business.objects.filter(business_id = business_id).exists():
            business_object = Business.objects.get(business_id = business_id)

        user_object = User.objects.get(username = headers["X-Email"])
        account_object = Account.objects.get(email = user_object)

        ### MISING TO VERIFY IF BUSINESS ALREADY HAS AN API KEY ###            

        new_generated_key = secrets.token_hex(16)
        if api_key_type == "TEST":
            api_key = "tsk_" + new_generated_key
        elif api_key_type == "PRODUCTION":
            api_key = "psk_" + new_generated_key

        new_api_key = ApiKey.objects.create(
            api_key = api_key,
            user_id = account_object,
            business_id = business_object if business_id else None,
            type = api_key_type,
            status = "INACTIVE"
            )
        
        response_object = {
            "status": "SUCCESS",
            "message": "API Key Created successfully",
            "data": {
                "customer_id": customer_id,
                "api_key": {
                    "api_key": new_api_key.api_key,
                    "business_id": new_api_key.business_id.business_id if business_id else None,
                    "type": api_key_type,
                    "status": "INACTIVE",
                }
            }
        }
        
        return Response(response_object, status=200)


class CreateApiKey_individual(APIView):
    def post(self, request):
        data = request.data["data"]
        headers = request.headers

        customer_id = headers.get("X-Customer-Id", None)
        business_id = data.get("business_id", None)
        api_key_type = data.get("type", None)

        # business_object = None
        if Business.objects.filter(business_id = business_id).exists():
            business_object = Business.objects.get(business_id = business_id)

        user_object = User.objects.get(username = headers["X-Email"])
        account_object = Insividual_Account.objects.get(email = user_object)

        ### MISING TO VERIFY IF BUSINESS ALREADY HAS AN API KEY ###            

        new_generated_key = secrets.token_hex(16)
        if api_key_type == "TEST":
            api_key = "tsk_" + new_generated_key
        elif api_key_type == "PRODUCTION":
            api_key = "psk_" + new_generated_key

        new_api_key = ApiKey.objects.create(
            api_key = api_key,
            user_id = account_object,
            business_id = business_object if business_id else None,
            type = api_key_type,
            status = "INACTIVE"
            )
        
        response_object = {
            "status": "SUCCESS",
            "message": "API Key Created successfully",
            "data": {
                "customer_id": customer_id,
                "api_key": {
                    "api_key": new_api_key.api_key,
                    "business_id": new_api_key.business_id.business_id if business_id else None,
                    "type": api_key_type,
                    "status": "INACTIVE",
                }
            }
        }
        
        return Response(response_object, status=200)



class GetApiKeys(APIView):
    def get(self, request):
        # data = request.data["data"]
        headers = request.headers

        customer_id = headers.get("X-Customer-Id", None)
        email = headers.get("X-Email", None)

        user_object = User.objects.get(
            username = email
        )

        account_object = Account.objects.get(email = user_object)
        api_key_objects = ApiKey.objects.filter(user_id = account_object)

        api_keys = []
        for api_key_object in api_key_objects:
            api_keys.append({
                "api_key": api_key_object.api_key,
                "business_id": api_key_object.business_id.business_id if api_key_object.business_id else None,
                "type": api_key_object.type,
                "status": api_key_object.status
            })

        response_object = {
            "status": "SUCCESS",
            "message": "API Key retrieved successfully",
            "data": {
                "customer_id": customer_id,
                "api_keys": api_keys
            }
        }

        return Response(response_object, status=200)

class GetApiKey(APIView):
    def get(self, request):
        headers = request.headers

        customer_id = headers.get("X-Customer-Id", None)
        email = headers.get("X-Email", None)
        business_id = headers.get("X-Business-Id", None)
        api_key_type = request.GET.get("type", None)


        user_object = User.objects.get(
            username = email
        )

        account_object = Account.objects.get(email = user_object)
        business_object = Business.objects.get(business_id = business_id)

        api_key_object = ApiKey.objects.filter(
            user_id = account_object,
            business_id = business_object,
            type = api_key_type
        )

        if api_key_object.exists():
            serializer = ApiKeysSerializer(api_key_object.first())
        else:
            serializer = None

        response_object = {
            "status": "SUCCESS",
            "message": "API Key retrieved successfully",
            "data": {
                "api_key": serializer.data if serializer else None
            }
        }

        return Response(response_object, status=200)





class Get_individual_ApiKey(APIView):
    def get(self, request):
        print('inside method Get_individual_ApiKey')
        headers = request.headers

        customer_id = headers.get("X-Customer-Id", None)
        email = headers.get("X-Email", None)
        # business_id = headers.get("X-Business-Id", None)
        api_key_type = request.GET.get("type", None)
        print('email')
        print(email)
        
        user_object = User.objects.get(
            username = email
        )

        account_object = Insividual_Account.objects.get(user_id = customer_id)
        # business_object = Business.objects.get(business_id = business_id)

        api_key_object = ApiKey_individual.objects.filter(
            user_id = account_object,
            # business_id = business_object,
            type = api_key_type
        )
        

        if api_key_object.exists():
            serializer = ApiKeysSerializer(api_key_object.first())
        else:
            serializer = None

        response_object = {
            "status": "SUCCESS",
            "message": "API Key retrieved successfully",
            "data": {
                "api_key": serializer.data if serializer else None
            }
        }

        return Response(response_object, status=200)






class ActivateApiKey(APIView):
    def post(self, request):
        data = request.data["data"]
        headers = request.headers

        customer_id = headers.get("X-Customer-Id", None)
        email = headers.get("X-Email", None)

        user_object = User.objects.get(
            username = email
        )

        account_object = Account.objects.get(email = user_object)
        api_key_object = ApiKey.objects.get(
            api_key = data["api_key"], 
            user_id = account_object
            )

        api_key_object.status = "ACTIVE"
        api_key_object.save()

        response_object = {
            "status": "SUCCESS",
            "message": "API Key activated successfully",
            "data": {
                "customer_id": customer_id,
                "api_key": api_key_object.api_key,
                "business_id": api_key_object.business_id.business_id if api_key_object.business_id else None,
                "type": api_key_object.type,
                "status": api_key_object.status
            }
        }

        return Response(response_object, status=200)

class DeactivateApiKey(APIView):
    def post(self, request):
        data = request.data["data"]
        headers = request.headers

        customer_id = headers.get("X-Customer-Id", None)
        email = headers.get("X-Email", None)

        user_object = User.objects.get(
            username = email
        )

        account_object = Account.objects.get(email = user_object)
        api_key_object = ApiKey.objects.get(
            api_key = data["api_key"], 
            user_id = account_object
            )

        api_key_object.status = "INACTIVE"
        api_key_object.save()

        response_object = {
            "status": "SUCCESS",
            "message": "API Key deactivated successfully",
            "data": {
                "customer_id": customer_id,
                "api_key": api_key_object.api_key,
                "business_id": api_key_object.business_id.business_id if api_key_object.business_id else None,
                "type": api_key_object.type,
                "status": api_key_object.status
            }
        }

        return Response(response_object, status=200)

#MISSING LINK TO API KEY TO BUSINESS
from django.shortcuts import render
from django.contrib import auth
from django.contrib.auth.models import User

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response  import Response
from rest_framework import status

from api_keys.models import Api_Key
from accounts.models import Account
from businesses.models import Business

import secrets

class CreateApiKey(APIView):
    def post(self, request):
        data = request.data
        headers = request.headers

        customer_id = headers.get("X-Customer-Id", None)
        business_id = data.get("business_id", None)
        api_key_type = data.get("type", None)

        # <<<---- Starts Verification ---->>>
        # <<<---- Starts Verification ---->>>
        # <<<---- Starts Verification ---->>>


        if not customer_id:
            return Response(
                {
                "status": "ERROR",
                "message": "X-Customer-Id not found"
                }, status=400)

        user_object = auth.authenticate(
            username = data["email"],
            password = data["password"]
        )

        if not user_object:
            return Response(
                {
                "status": "ERROR",
                "message": "Invalid credentials"
                }, status=400)

        # <<<---- Ends Verification ---->>>
        # <<<---- Ends Verification ---->>>
        # <<<---- Ends Verification ---->>>


        if Business.objects.filter(business_id = business_id).exists():
            business_object = Business.objects.get(business_id = business_id)

        #VERIFY IF BUSINESS ALREADY HAS API KEY
        if Api_Key.objects.filter(business_id = business_object, type = api_key_type).exists():
            return Response(
                {
                "status": "ERROR",
                "message": "Business already has an API Key"
                }, status=400)
            

        new_generated_key = secrets.token_hex(16)
        if api_key_type == "TEST":
            api_key = "tsk_" + new_generated_key
        elif api_key_type == "PRODUCTION":
            api_key = "psk_" + new_generated_key

        account_object = Account.objects.get(user_id = user_object)

        new_api_key = Api_Key.objects.create(
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
                "api_keys": [
                    {
                        "api_key": new_api_key.api_key,
                        "business_id": new_api_key.business_id.business_id if business_object else None,
                        "type": api_key_type,
                        "status": "INACTIVE",
                    }
                ]
            }
        }
        
        return Response(response_object, status=200)


class GetApiKeys(APIView):
    def post(self, request):
        data = request.data
        headers = request.headers

        customer_id = headers.get("X-Customer-Id", None)

        if not customer_id:
            return Response(
                {
                "status": "ERROR",
                "message": "X-Customer-Id not found"
                }, status=400)

        user_object = auth.authenticate(
            username = data["email"],
            password = data["password"]
        )

        if not user_object:
            return Response(
                {
                "status": "ERROR",
                "message": "Invalid credentials"
                }, status=400)

        account_object = Account.objects.get(email = user_object)

        api_key_objects = Api_Key.objects.filter(user_id = account_object)

        api_keys = []

        for api_key_object in api_key_objects:
            api_keys.append({
                "api_key": api_key_object.api_key,
                "business_id": api_key_object.business_id.business_id,
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

class ActivateApiKey(APIView):
    def post(self, request):
        data = request.data
        headers = request.headers

        customer_id = headers.get("X-Customer-Id", None)

        if not customer_id:
            return Response(
                {
                "status": "ERROR",
                "message": "X-Customer-Id not found"
                }, status=400)

        user_object = auth.authenticate(
            username = data["email"],
            password = data["password"]
        )

        if not user_object:
            return Response(
                {
                "status": "ERROR",
                "message": "Invalid credentials"
                }, status=400)

        account_object = Account.objects.get(email = user_object)

        api_key_object = Api_Key.objects.get(
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
                "business_id": api_key_object.business_id.business_id,
                "type": api_key_object.type,
                "status": api_key_object.status
            }
        }

        return Response(response_object, status=200)

class DeactivateApiKey(APIView):
    def post(self, request):
        data = request.data
        headers = request.headers

        customer_id = headers.get("X-Customer-Id", None)

        if not customer_id:
            return Response(
                {
                "status": "ERROR",
                "message": "X-Customer-Id not found"
                }, status=400)

        user_object = auth.authenticate(
            username = data["email"],
            password = data["password"]
        )

        if not user_object:
            return Response(
                {
                "status": "ERROR",
                "message": "Invalid credentials"
                }, status=400)

        account_object = Account.objects.get(email = user_object)

        api_key_object = Api_Key.objects.get(
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
                "business_id": api_key_object.business_id.business_id,
                "type": api_key_object.type,
                "status": api_key_object.status
            }
        }

        return Response(response_object, status=200)
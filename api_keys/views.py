from django.shortcuts import render
from django.contrib import auth
from django.contrib.auth.models import User

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response  import Response
from rest_framework import status

from api_keys.models import Api_Key
from accounts.models import Account


class GetApiKeys(APIView):
    def post(self, request):
        data = request.data
        headers = request.headers

        customer_id = headers.get("customer_id", None)

        if not customer_id:
            return Response({"error": "customer_id not found"}, status=400)

        user_object = auth.authenticate(
            username = data["email"],
            password = data["password"]
        )

        if not user_object:
            return Response({"error": "Invalid credentials"}, status=400)

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
                "customer_id": "YOUR-CUSTOMER-ID",
                "api_keys": api_keys
            }
        }

        return Response(response_object, status=200)
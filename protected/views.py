from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth.models import User

from transactions.models import Transaction, TransactionBook ,TransactionIns
from cryptocurrency.models import Address, Blockchain, Cryptocurrency, Network

from accounts.models import Account
from api_keys.models import ApiKey

# from rest_framework import Response
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.response  import Response
from rest_framework import status

import json


class EmailHasAccount(APIView):
    def post(self, request):
        data = request.data["data"]
        user_object = None

        response_object = {
            "status": "SUCCESS",
            "message": "",
            "data": {
                "email_is_available": None,
                "type": None
            }
        }



        if User.objects.filter(email = data["email"]).exists():
            response_object["message"] = "Email already exists"
            response_object["data"]["email_is_available"] = False

            user_object = User.objects.get(email = data["email"])

            account_object = Account.objects.get(email = user_object)

            response_object["data"]["type"] = account_object.type

        else:
            response_object["message"] = "Email is available"
            response_object["data"]["email_is_available"] = True



        return Response(response_object, status=200)

class GetAPIKeyNoAccount(APIView):
    def get(self, request, type):
        headers = request.headers


        email = headers["X-Email"]

        if not User.objects.filter(email = email).exists():
            return Response(
                {
                "status": "ERROR",
                "message": "Invalid email"
                }, status=400)

        user = User.objects.get(email = email)

        account = Account.objects.filter(email = user, type = "NO_ACCOUNT")

        if not account.exists():
            return Response(
                {
                "status": "ERROR",
                "message": "Invalid email, user has an official account"
                }, status=400)

        account = account.first()
        

        if not ApiKey.objects.filter(user_id = account, type = type).exists():
            return Response(
                {
                "status": "ERROR",
                "message": "API Key does not exist"
                }, status=400)


        api_key_object = ApiKey.objects.get(
            user_id = account,
            type = type
        )

        response_object = {
            "status": "SUCCESS",
            "message": "API Key retrieved successfully",
            "data": {
                "api_key": api_key_object.api_key,
                "type": api_key_object.type
            }
        }
        
        return Response(response_object, status=200)
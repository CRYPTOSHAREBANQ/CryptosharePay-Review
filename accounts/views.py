from django.shortcuts import render
from django.contrib import auth
from django.contrib.auth.models import User
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

from accounts.models import Account, Country
from businesses.models import Business
from api_keys.models import Api_Key

# from rest_framework import Response
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.response  import Response
from rest_framework import status

import secrets

# Create your views here.

# @csrf_exempt
# @api_view(['GET', 'POST'])
class CreateAccount(APIView):
    def post(self, request):
        # print(request.data, request.headers)
        data = request.data

        customer_info = data["customer_info"]
        business_info = data.get("business_info", None)

        if User.objects.filter(email = customer_info["email"]).exists():
            return Response(
                {
                "status": "ERROR",
                "message": "Email already exists"
                }, status=400)
        
        if customer_info["password"] != customer_info["confirm_password"]:
            return Response(
                {
                "status": "ERROR",
                "message": "Passwords do not match"
                }, status=400)

        if Country.objects.filter(country_id = data['country_id']).exists():
            return Response(
                {
                "status": "ERROR",
                "message": "Country Code does not exist"
                }, status=400)

        new_user = User.objects.create_user(
            username = data['email'], 
            password = data['password'], 
            email = data['email'],
            first_name = data['first_name'],
            last_name = data['last_name']
            )

        new_account = Account.objects.create(
            type = "CUSTOMER", 
            email = new_user, 
            first_name = data['first_name'], 
            last_name = data['last_name'], 
            country_id = Country.objects.get(
                country_id=data['country_id']
                )
            )

        if business_info:
            new_business = Business.objects.create(
                user_id = new_account, 
                name = business_info['name'], 
                description = business_info['description']
                )

        new_generated_key = secrets.token_hex(16)

        new_api_key = Api_Key.objects.create(
            api_key = "tsk_" + new_generated_key,
            user_id = new_account,
            business_id = new_business if business_info else None,
            type = "TEST",
            status = "INACTIVE"
            )

        
        response_object = {
            "status": "SUCCESS",
            "message": "Customer created successfully",
            "data": {
                "api_key": new_api_key.api_key,
                "account_id": new_account.user_id,
                "business_id": new_business.business_id if business_info else None
            }
        }

        return Response(response_object, status=status.HTTP_200_OK)


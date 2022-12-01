from django.shortcuts import render
from django.contrib.auth.models import User
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

from accounts.models import Account, Country
from businesses.models import Business
from api_keys.models import ApiKey

# from rest_framework import Response
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.response  import Response
from rest_framework import status

from common_libraries.general.general_utils import generate_pin
from common_libraries.emails.email_client import EmailClient

from businesses.serializers import BusinessesSerializer

import secrets
from datetime import datetime
# Create your views here.

# @csrf_exempt
# @api_view(['GET', 'POST'])
class CreateAccount(APIView):
    def post(self, request):
        # print(request.data, request.headers)

        data = request.data["data"]

        customer_info = data["customer_info"]
        business_info = data.get("business_info", None)

        new_user = User.objects.create_user(
            username = customer_info['email'], 
            password = customer_info['password'], 
            email = customer_info['email'].lower(),
            first_name = customer_info['first_name'],
            last_name = customer_info['last_name'],
        )

        new_account = Account.objects.create(
            type = customer_info["type"], 
            email = new_user, 
            first_name = customer_info['first_name'], 
            last_name = customer_info['last_name'], 
            birthdate = datetime.strptime(customer_info['birthdate'], '%Y-%m-%d'),
            country_id = Country.objects.get(
                country_id=customer_info['country_id']
                )
        )

        if business_info:
            new_business = Business.objects.create(
                user_id = new_account, 
                name = business_info['name'], 
                description = business_info['description']
                )

        new_generated_key = secrets.token_hex(16)

        # api_key_prefix = "tsk_"
        # api_key_type = "TEST"
        # api_key_status = "INACTIVE"

        api_key_prefix = "psk_"
        api_key_type = "PRODUCTION"
        api_key_status = "ACTIVE"

        if customer_info["type"] == "NO_ACCOUNT":
            api_key_prefix = "psk_"
            api_key_type = "PRODUCTION"
            api_key_status = "ACTIVE"

        new_api_key = ApiKey.objects.create(
            api_key = api_key_prefix + new_generated_key,
            user_id = new_account,
            business_id = new_business if business_info else None,
            type = api_key_type,
            status = api_key_status
        )

        
        response_object = {
            "status": "SUCCESS",
            "message": "Customer created successfully",
            "data": {
                "api_key": new_api_key.api_key,
                "customer_id": new_account.user_id,
                "business_id": new_business.business_id if business_info else None
            }
        }

        return Response(response_object, status=200)

class RequestCustomerID(APIView):
    def post(self, request):
        headers = request.headers

        email = headers.get("X-Email", None)
        password = headers.get("X-Password", None)

        user_object = User.objects.get(email = email)

        account_object = Account.objects.get(email = user_object)

        new_pin = generate_pin()

        account_object.security_pin = new_pin
        account_object.save()

        email_client = EmailClient()
        email_client.request_customer_id(new_pin, email)

        response_object = {
            "status": "SUCCESS",
            "message": "Customer ID requested successfully, please verify your email"
        }

        return Response(response_object, status=200)

class GetAccountCustomerID(APIView):
    def get(self, request):
        headers = request.headers

        email = headers.get("X-Email", None)

        user_object = User.objects.get(email = email)
        account_object = Account.objects.get(email = user_object)

        response_object = {
            "status": "SUCCESS",
            "message": "Customer ID retrieved successfully",
            "data": {
                "customer_id": account_object.user_id
            }
        }

        account_object.security_pin = None
        account_object.save()

        return Response(response_object, status=200)

class GetAccount(APIView):
    def get(self, request):
        headers = request.headers

        email = headers.get("X-Email", None)

        user_object = User.objects.get(email = email)
        account_object = Account.objects.get(email = user_object)

        businesses = Business.objects.filter(user_id = account_object)

        serializer = BusinessesSerializer(businesses, many=True)

        response_object = {
            "status": "SUCCESS",
            "message": "Account info retrieved successfully",
            "data": {
                "first_name": account_object.first_name,
                "last_name": account_object.last_name,
                "email": account_object.email.email,
                "country_id": account_object.country_id.country_id,
                "businesses": serializer.data if serializer else None
            }
        }

        return Response(response_object, status=200)
        
        





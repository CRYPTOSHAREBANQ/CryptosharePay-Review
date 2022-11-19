from django.shortcuts import render
from django.contrib.auth.models import User

from accounts.models import Account
from businesses.models import Business
from cryptocurrency.models import Blockchain, Cryptocurrency, Network

from businesses.serializers import BusinessesSerializer

from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.response  import Response
from rest_framework import status
# Create your views here.

class GetBusinesses(APIView):
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
                "businesses": serializer.data if serializer else None
            }
        }

        return Response(response_object, status=200)
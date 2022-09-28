from django.shortcuts import render
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


class CreateTransaction(APIView):
    def post(self, request):
        
        pass
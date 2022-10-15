#Import django http response
from django.http import HttpResponse
from django.shortcuts import render
from digital_currency.models import DigitalCurrency
from digital_currency.serializers import DigitalCurrenciesSerializer, DigitalCurrencySerializer

from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.response  import Response
from rest_framework import status
# Create your views here.

class Ping(APIView):
    def get(self, request):
        # Return 200 code with Django Rest Framework
        return Response(status=200)

def cryptoapis_verification(request):

    return HttpResponse("cryptoapis-cb-8eed1de04dc9ecb0cea21afb0351d0cefa6417c4e7a221747c6aa36c53854448")
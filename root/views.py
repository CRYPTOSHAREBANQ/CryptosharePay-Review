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

    return HttpResponse("cryptoapis-cb-94e7e1b0d5c6f9b449ef0cea3371a4dc02f215518cc95fd8bc07825a54811d33")
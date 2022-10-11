from django.shortcuts import render
from digital_currency.models import DigitalCurrency
from digital_currency.serializers import DigitalCurrenciesSerializer, DigitalCurrencySerializer

from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.response  import Response
from rest_framework import status
# Create your views here.


class GetDigitalCurrencies(APIView):
    def get(self, request):
        
        digital_currencies = DigitalCurrency.objects.all()
        
        serializer = DigitalCurrenciesSerializer(digital_currencies, many=True)

        response_object = {
            "status": "SUCCESS",
            "message": "Digital Currencies retrieved successfully",
            "data": {
                "digital_currencies": serializer.data
            }
        }

        return Response(response_object, status=200)

class GetDigitalCurrency(APIView):
    def get(self, request, code):
        digital_currency = DigitalCurrency.objects.filter(digital_currency_id = code)
        digital_currency = digital_currency.first()

        if digital_currency:
            serializer = DigitalCurrencySerializer(digital_currency)
        else:
            serializer = None

        response_object = {
            "status": "SUCCESS",
            "message": "Digital Currency retrieved successfully",
            "data": {
                "digital_currency": serializer.data if serializer else None
            }
        }

        return Response(response_object, status=200)
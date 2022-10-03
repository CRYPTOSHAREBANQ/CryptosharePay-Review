from django.shortcuts import render

from .serializers import CryptocurrenciesSerializer, CryptocurrencySerializer

from cryptocurrency.models import Cryptocurrency

from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.response  import Response
from rest_framework import status
# Create your views here.

class GetCryptocurrencies(APIView):
    def get(self, request):

        cryptocurrencies = Cryptocurrency.objects.all().order_by("network_id__network_id")

        serializer = CryptocurrenciesSerializer(cryptocurrencies, many=True)

        response_object = {
            "status": "SUCCESS",
            "message": "Cryptocurrencies retrieved successfully",
            "data": {
                "cryptocurrencies": serializer.data
            }
        }

        return Response(response_object, status=200)

class GetCryptocurrency(APIView):
    def get(self, request, code, network):

        cryptocurrency = Cryptocurrency.objects.filter(symbol = code, network_id__network_id = network)
        cryptocurrency = cryptocurrency.first()

        if cryptocurrency:
            serializer = CryptocurrencySerializer(cryptocurrency)
        else:
            serializer = None


        response_object = {
            "status": "SUCCESS",
            "message": "Cryptocurrency retrieved successfully",
            "data": {
                "cryptocurrency": serializer.data if serializer else None
            }
        }

        return Response(response_object, status=200)
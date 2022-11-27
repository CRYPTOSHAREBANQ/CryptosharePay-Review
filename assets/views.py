from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response  import Response
from rest_framework import status

from api_keys.models import ApiKey
from assets.models import Asset

from assets.serializers import AssetSerializer, AssetsSerializer

class GetAssets(APIView):
    def get(self, request):
        headers = request.headers

        api_key = headers.get("X-API-Key", None)
        api_key_object = ApiKey.objects.get(api_key = api_key)

        assets = Asset.objects.filter(api_key = api_key_object)

        serializer = AssetsSerializer(assets, many=True)

        response_object = {
            "status": "SUCCESS",
            "message": "Assets retrieved successfully",
            "data": {
                "assets": serializer.data
            }
        }

        return Response(response_object, status = 200)

class GetAsset(APIView):
    def get(self, request, cryptocurrency_code):
        headers = request.headers

        api_key = headers.get("X-API-Key", None)
        api_key_object = ApiKey.objects.get(api_key = api_key)
        
        try:
            asset = Asset.objects.get(api_key = api_key_object, cryptocurrency_id__symbol = cryptocurrency_code)

            serializer = AssetSerializer(asset)
        except:
            pass

        response_object = {
            "status": "SUCCESS",
            "message": "Asset retrieved successfully",
            "data": {
                "asset": serializer.data if "serializer" not in locals() else []
            }
        }

        return Response(response_object, status = 200)
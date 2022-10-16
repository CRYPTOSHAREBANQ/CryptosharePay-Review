from django.db import models
from api_keys.models import ApiKey
from cryptocurrency.models import Cryptocurrency

from rest_framework.views import APIView
from rest_framework.response  import Response
from rest_framework import status

from api_keys.models import ApiKey
from accounts.models import Account
from businesses.models import Business

class Asset(models.Model):
    api_key = models.ForeignKey(ApiKey, on_delete=models.CASCADE)
    type = models.CharField(max_length=12)
    cryptocurrency_id = models.ForeignKey(Cryptocurrency, on_delete=models.PROTECT)
    amount = models.DecimalField(max_digits=20, decimal_places=8)
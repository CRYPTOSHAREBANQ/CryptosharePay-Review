from django.db import models

import uuid
from api_keys.models import Api_Key

# Create your models here.

class Network(models.Model):
    network_id = models.CharField(max_length=21, primary_key=True)
    name = models.CharField(max_length=30)

class Blockchain(models.Model):
    blockchain_id = models.CharField(max_length=21, primary_key=True)
    name = models.CharField(max_length=30)

class Cryptocurrency(models.Model):
    cryptocurrency_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    blockchain_id = models.ForeignKey(Blockchain, on_delete=models.PROTECT, null=True)
    network_id = models.ForeignKey(Network, on_delete=models.PROTECT, null=True)
    type = models.CharField(max_length=8)
    name = models.CharField(max_length=50)
    coingecko_name = models.CharField(max_length=50, null=True)
    symbol = models.CharField(max_length=10)
    exchange_rate = models.DecimalField(max_digits=20, decimal_places=8)

class Address_Subscription(models.Model):
    subscription_id = models.CharField(max_length=36, primary_key=True)
    event = models.CharField(max_length=40)
    blockchain_id = models.ForeignKey(Blockchain, on_delete=models.PROTECT, null=True)
    network_id = models.ForeignKey(Network, on_delete=models.PROTECT, null=True)
    creation_datetime = models.DateTimeField(auto_now_add=True)
    callback_url = models.URLField(max_length=200)

class Address(models.Model):
    address_id = models.CharField(max_length=60, primary_key=True)
    address = models.CharField(max_length=100)
    api_key = models.ForeignKey(Api_Key, on_delete=models.SET_NULL, null=True)
    cryptocurrency_id = models.ForeignKey(Cryptocurrency, on_delete=models.SET_NULL, null=True)
    subscription_id = models.ForeignKey(Address_Subscription, on_delete=models.SET_NULL, null=True)
    status = models.CharField(max_length=15)
    

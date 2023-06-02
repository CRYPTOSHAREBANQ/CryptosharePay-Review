from django.db import models

import uuid
from django.contrib.auth.models import User

# Create your models here.

class Country(models.Model):
    country_id = models.CharField(max_length=3, primary_key=True)
    country_name = models.CharField(max_length=57)
    status = models.CharField(max_length=15)

class Account(models.Model):
    user_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    type = models.CharField(max_length=15)
    email = models.ForeignKey(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    country_id = models.ForeignKey(Country, on_delete=models.CASCADE)
    birthdate = models.DateField(null=True)
    cryptosharecredit_linked = models.BooleanField(default=False)
    cryptosharecredit_email = models.EmailField(max_length = 254, null=True)
    cryptosharecredit_username = models.CharField(max_length=30, null=True)
    security_pin = models.CharField(max_length=6, null=True)
    random_password = models.CharField(max_length=16, null=True)
    status = models.CharField(max_length=15, default="ACTIVE")

class Document(models.Model):
    user_id = models.ForeignKey(Account, on_delete=models.CASCADE)
    name = models.CharField(max_length=254)
    type = models.CharField(max_length=25)
    s3_url = models.CharField(max_length=254)
    
    
    
class Insividual_Account(models.Model):
    user_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    email = models.ForeignKey(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=30)
    identity = models.CharField(max_length=30)
    phone = models.CharField(max_length=30)
    cadula = models.CharField(max_length=200)
    country_id = models.ForeignKey(Country, on_delete=models.CASCADE)
    birthdate = models.DateField(null=True)
    cryptosharecredit_linked = models.BooleanField(default=False)
    cryptosharecredit_email = models.EmailField(max_length = 254, null=True)
    cryptosharecredit_username = models.CharField(max_length=30, null=True)
    security_pin = models.CharField(max_length=6, null=True)
    random_password = models.CharField(max_length=16, null=True)
    status = models.CharField(max_length=15, default="ACTIVE")
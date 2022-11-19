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
    cryptosharecredit_linked = models.BooleanField(default=False)
    cryptosharecredit_email = models.EmailField(max_length = 254, null=True)
    cryptosharecredit_username = models.CharField(max_length=30, null=True)
    security_pin = models.CharField(max_length=6, null=True)
    random_password = models.CharField(max_length=16, null=True)
    status = models.CharField(max_length=15, default="ACTIVE")
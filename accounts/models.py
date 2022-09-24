from django.db import models

import uuid
from django.contrib.auth.models import User

# Create your models here.

class Country(models.Model):
    country_id = models.CharField(max_length=3, primary_key=True)
    country_name = models.CharField(max_length=57)

class Account(models.Model):
    user_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    type = models.CharField(max_length=15)
    email = models.ForeignKey(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    country_id = models.ForeignKey(Country, on_delete=models.CASCADE)
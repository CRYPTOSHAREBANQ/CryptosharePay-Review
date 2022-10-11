from django.db import models
from accounts.models import Account
import uuid

# Create your models here.

class Business(models.Model):
    business_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user_id = models.ForeignKey(Account, on_delete=models.CASCADE)
    name = models.CharField(max_length=57)
    description = models.CharField(max_length=32)
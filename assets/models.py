from django.db import models
from api_keys.models import ApiKey
from cryptocurrency.models import Cryptocurrency

# Create your models here

class Asset(models.Model):
    api_key = models.ForeignKey(ApiKey, on_delete=models.CASCADE)
    type = models.CharField(max_length=12)
    amount = models.DecimalField(max_digits=20, decimal_places=8)
    cryptocurrency_id = models.ForeignKey(Cryptocurrency, on_delete=models.PROTECT)
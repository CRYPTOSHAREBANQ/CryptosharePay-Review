from django.db import models
from accounts.models import Account
from businesses.models import Business


# Create your models here.
class Api_Key(models.Model):
    api_key = models.CharField(max_length=100, primary_key=True)
    user_id = models.ForeignKey(Account, on_delete=models.CASCADE)
    business_id = models.ForeignKey(Business, on_delete=models.CASCADE, null=True)
    type = models.CharField(max_length=15)
    status = models.CharField(max_length=10)

class Assets(models.Model):
    api_key = models.ForeignKey(Api_Key, on_delete=models.CASCADE)
    type = models.CharField(max_length=12)
    amount = models.DecimalField(max_digits=20, decimal_places=8)
    cryptocurrency_id = models.ForeignKey("cryptocurrency.Cryptocurrency", on_delete=models.PROTECT)
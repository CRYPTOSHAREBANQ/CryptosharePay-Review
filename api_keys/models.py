from django.db import models
from accounts.models import Account,Insividual_Account
from businesses.models import Business


# Create your models here.
class ApiKey(models.Model):
    api_key = models.CharField(max_length=100, primary_key=True)
    user_id = models.ForeignKey(Account, on_delete=models.CASCADE)
    business_id = models.ForeignKey(Business, on_delete=models.CASCADE, null=True)
    type = models.CharField(max_length=15)
    status = models.CharField(max_length=10)
    
    
    
class ApiKey_individual(models.Model):
    api_key = models.CharField(max_length=100, primary_key=True)
    user_id = models.ForeignKey(Insividual_Account, on_delete=models.CASCADE)
    business_id = models.ForeignKey(Business, on_delete=models.CASCADE, null=True)
    type = models.CharField(max_length=15)
    status = models.CharField(max_length=10)
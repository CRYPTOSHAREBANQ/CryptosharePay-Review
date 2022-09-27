from django.db import models

# Create your models here.

class Digital_Currency(models.Model):
    digital_currency_id = models.CharField(max_length=4, primary_key=True)
    digital_currency_name = models.CharField(max_length=50)
    exchange_rate = models.DecimalField(max_digits=8, decimal_places=2)
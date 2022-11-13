from django.db import models

import uuid
from api_keys.models import ApiKey
from cryptocurrency.models import Cryptocurrency, Address, StaticAddress
from digital_currency.models import DigitalCurrency

from django.utils import timezone
from datetime import datetime, timedelta
# Create your models here.


class AutomatedTransaction(models.Model):
    transaction_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    api_key = models.ForeignKey(ApiKey, on_delete=models.CASCADE)
    status = models.CharField(max_length=15)
    description = models.CharField(max_length=100, null=True)
    type = models.CharField(max_length=12)
    frecuency = models.CharField(max_length=7)
    scheduled_day = models.CharField(max_length=12)

    funds_source_type = models.CharField(max_length=30, default="DEPOSIT_ADDRESS")
    funds_source_address = models.CharField(max_length=100, null=True)
    funds_source_address_object = models.ForeignKey(StaticAddress, on_delete=models.PROTECT, null=True)

    digital_currency_id = models.ForeignKey(DigitalCurrency, on_delete=models.PROTECT, null=True)
    digital_currency_amount = models.DecimalField(max_digits=14, decimal_places=2, null=True)
    cryptocurrency_id = models.ForeignKey(Cryptocurrency, on_delete=models.SET_NULL, null=True)
    cryptocurrency_id_amount = models.DecimalField(max_digits=14, decimal_places=2, null=True)
    
    receiver_address = models.CharField(max_length=100, null=True)
    client_email = models.EmailField(max_length = 254, null=True)
    client_phone = models.CharField(max_length=20, null=True)

    creation_datetime = models.DateTimeField(auto_now_add=True)
    last_event_datetime = models.DateTimeField(null = True)
    next_event_datetime = models.DateTimeField(null = True)

class Transaction(models.Model):
    def set_expiration_datetime():
        return timezone.now()+timedelta(days=1)

    transaction_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    api_key = models.ForeignKey(ApiKey, on_delete=models.CASCADE)
    type = models.CharField(max_length=20)
    description = models.CharField(max_length=100, null=True)
    digital_currency_id = models.ForeignKey(DigitalCurrency, on_delete=models.PROTECT, null=True)
    digital_currency_amount = models.DecimalField(max_digits=14, decimal_places=2, null=True)
    cryptocurrency_amount = models.DecimalField(max_digits=20, decimal_places=8, null=True)
    cryptocurrency_amount_received = models.DecimalField(max_digits=20, decimal_places=8, default=0, null=True)
    address_id = models.ForeignKey(Address, on_delete=models.PROTECT, null=True)
    withdrawal_address = models.CharField(max_length=100, null=True)
    address_refund = models.CharField(max_length=100, null=True)
    client_email = models.EmailField(max_length = 254, null=True)
    client_phone = models.CharField(max_length=20, null=True)
    creation_datetime = models.DateTimeField(auto_now_add=True)
    expiration_datetime = models.DateTimeField(default=set_expiration_datetime(), null= True)
    state = models.CharField(max_length=20, null=True)
    status = models.CharField(max_length=20, null=True)

class TransactionIns(models.Model):
    transaction_ins_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    external_transaction_id = models.CharField(max_length=100, null=True)
    amount = models.DecimalField(max_digits=20, decimal_places=8)
    address_id = models.ForeignKey(Address, on_delete=models.PROTECT)
    creation_datetime = models.DateTimeField(auto_now_add=True)
    completed_datetime = models.DateTimeField(null=True)
    state = models.CharField(max_length=15)
    status = models.CharField(max_length=15)

class TransactionOuts(models.Model):
    transaction_ins_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    external_transaction_id = models.CharField(max_length=100, null=True)
    amount = models.DecimalField(max_digits=20, decimal_places=8)
    address_id = models.ForeignKey(Address, on_delete=models.PROTECT)
    address_out = models.CharField(max_length=100, null= True)
    creation_datetime = models.DateTimeField(auto_now_add=True)
    completed_datetime = models.DateTimeField(null=True)
    state = models.CharField(max_length=15)
    status = models.CharField(max_length=15)

class TransactionBook(models.Model):
    registry_id = models.AutoField(primary_key=True)
    type = models.CharField(max_length=5)
    transaction_id = models.ForeignKey(Transaction, on_delete=models.PROTECT)
    transaction_ins_id = models.ForeignKey(TransactionIns, on_delete=models.PROTECT, null=True)
    transaction_outs_id = models.ForeignKey(TransactionOuts, on_delete=models.PROTECT, null=True)
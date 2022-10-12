from rest_framework import serializers
from .models import DigitalCurrency

class TransactionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = DigitalCurrency
        fields = '__all__'

    def to_representation(self, instance):
        return {
            "transaction_id": instance.transaction_id,
            "transaction_type": instance.type,
            "description": instance.description,
            "digital_currency_code": instance.digital_currency_id.digital_currency_id,
            "digital_currency_amount": instance.digital_currency_amount,
            "cryptocurrency_code": instance.address_id.cryptocurrency_id.symbol,
            "cryptocurrency_amount": instance.cryptocurrency_amount,
            "cryptocurrency_amount_received": instance.cryptocurrency_amount_received,
            "address": instance.address_id.address,
            "client_email": instance.client_email,
            "client_phone": instance.client_phone,
            "creation_datetime": instance.creation_datetime,
            "expiration_datetime": instance.expiration_datetime,
            "status": instance.status
        }

class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = DigitalCurrency
        fields = '__all__'

    def to_representation(self, instance):
        return {
            "transaction_id": instance.transaction_id,
            "transaction_type": instance.type,
            "description": instance.description,
            "digital_currency_code": instance.digital_currency_id.digital_currency_id,
            "digital_currency_amount": instance.digital_currency_amount,
            "cryptocurrency_code": instance.address_id.cryptocurrency_id.symbol,
            "cryptocurrency_amount": instance.cryptocurrency_amount,
            "cryptocurrency_amount_received": instance.cryptocurrency_amount_received,
            "address": instance.address_id.address,
            "client_email": instance.client_email,
            "client_phone": instance.client_phone,
            "creation_datetime": instance.creation_datetime,
            "expiration_datetime": instance.expiration_datetime,
            "status": instance.status
        }
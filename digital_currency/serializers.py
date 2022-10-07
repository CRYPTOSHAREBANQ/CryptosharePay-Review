from rest_framework import serializers
from .models import DigitalCurrency

class DigitalCurrenciesSerializer(serializers.ModelSerializer):
    class Meta:
        model = DigitalCurrency
        fields = '__all__'

    def to_representation(self, instance):
        return {
            "code": instance.digital_currency_id,
            "name": instance.name
        }

class DigitalCurrencySerializer(serializers.ModelSerializer):
    class Meta:
        model = DigitalCurrency
        fields = '__all__'

    def to_representation(self, instance):
        return {
            "code": instance.digital_currency_id,
            "name": instance.name,
            "exchange_rate": instance.exchange_rate
        }
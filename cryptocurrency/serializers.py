from rest_framework import serializers
from .models import Cryptocurrency

class CryptocurrenciesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cryptocurrency
        fields = '__all__'

    def to_representation(self, instance):
        return {
            "code": instance.symbol,
            "name": instance.name,
            "type": instance.type,
            "blockchain": instance.blockchain_id.blockchain_id,
            "network": instance.network_id.network_id,
        }

class CryptocurrencySerializer(serializers.ModelSerializer):
    class Meta:
        model = Cryptocurrency
        fields = '__all__'

    def to_representation(self, instance):
        return {
            "code": instance.symbol,
            "name": instance.name,
            "type": instance.type,
            "blockchain": instance.blockchain_id.blockchain_id,
            "network": instance.network_id.network_id,
            "exchange_rate": instance.exchange_rate,
        }
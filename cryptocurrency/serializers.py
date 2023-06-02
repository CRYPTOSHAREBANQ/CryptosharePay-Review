from rest_framework import serializers
from .models import Blockchain, Cryptocurrency, Network

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

class BlockchainsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Blockchain
        fields = '__all__'

    def to_representation(self, instance):
        return {
            "blockchain_id": instance.blockchain_id,
            "name": instance.name,
        }

class NetworksSerializer(serializers.ModelSerializer):
    class Meta:
        model = Network
        fields = '__all__'
    
    def to_representation(self, instance):
        return {
            "network_id": instance.network_id,
            "name": instance.name,
        }
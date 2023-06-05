from rest_framework import serializers
from .models import Asset


class AssetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Asset
        fields = '__all__'
    
    def to_representation(self, instance):
        return {
            "cryptocurrency": instance.cryptocurrency_id.symbol,
            "amount": instance.amount
        }   

class AssetsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Asset
        fields = '__all__'
    
    def to_representation(self, instance):
        return {
            "cryptocurrency": instance.cryptocurrency_id.symbol,
            "amount": instance.amount
        }
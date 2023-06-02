from rest_framework import serializers
from .models import ApiKey


class ApiKeysSerializer(serializers.ModelSerializer):
    class Meta:
        model = ApiKey
        fields = '__all__'

    def to_representation(self, instance):
        return {
            "api_key": instance.api_key,
            "business_id": instance.business_id.business_id if instance.business_id else None,
            "type": instance.type,
            "status": instance.status
        }
from rest_framework import serializers
from .models import Business


class BusinessesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Business
        fields = '__all__'

    def to_representation(self, instance):
        return {
            "business_id": instance.business_id,
            "name": instance.name,
            "description": instance.description
        }
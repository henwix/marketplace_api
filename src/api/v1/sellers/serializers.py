from rest_framework import serializers

from src.apps.sellers.models import Seller


class SellerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Seller
        fields = ['id', 'name', 'description', 'avatar', 'background']
        read_only_fields = ['id', 'avatar', 'background']

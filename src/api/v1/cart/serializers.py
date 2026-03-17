from rest_framework import serializers

from src.api.v1.common.serializers import BaseInSerializer


class AddCartItemInSerializer(BaseInSerializer):
    product_variant_id = serializers.UUIDField()
    quantity = serializers.IntegerField(min_value=1, max_value=2147483647)


class DeleteCartItemInSerializer(BaseInSerializer):
    product_variant_id = serializers.UUIDField()


class CartItemOutSerializer(serializers.Serializer):
    product_variant_id = serializers.UUIDField()
    quantity = serializers.IntegerField(min_value=1, max_value=2147483647)
    price_snapshot = serializers.DecimalField(max_digits=10, decimal_places=2)
    created_at = serializers.DateTimeField()

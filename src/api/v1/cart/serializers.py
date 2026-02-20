from rest_framework import serializers

from src.apps.cart.models import CartItem


class AddItemToCartInSerializer(serializers.Serializer):
    product_variant_id = serializers.UUIDField()
    quantity = serializers.IntegerField(min_value=1, max_value=2147483647)


# TODO: use serializers.Serializer
class CartItemOutSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = ['product_variant_id', 'quantity', 'price_snapshot', 'created_at']

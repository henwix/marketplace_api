from rest_framework import serializers


class AddItemToCartInSerializer(serializers.Serializer):
    product_variant_id = serializers.UUIDField()
    quantity = serializers.IntegerField(min_value=1, max_value=2147483647)

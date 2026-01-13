from decimal import Decimal

from rest_framework import serializers


class CreateProductVariantInSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=200)
    price = serializers.DecimalField(max_digits=10, decimal_places=2, min_value=Decimal('0.10'))
    stock = serializers.IntegerField(min_value=0, max_value=2147483647, default=0)
    is_visible = serializers.BooleanField(default=True)


class UpdateProductVariantInSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=200)
    price = serializers.DecimalField(max_digits=10, decimal_places=2, min_value=Decimal('0.10'))
    stock = serializers.IntegerField(min_value=0, max_value=2147483647)
    is_visible = serializers.BooleanField()


class ProductVariantOutSerializer(serializers.Serializer):
    id = serializers.UUIDField()
    title = serializers.CharField(max_length=200)
    price = serializers.DecimalField(max_digits=10, decimal_places=2)
    stock = serializers.IntegerField(min_value=0, max_value=2147483647)
    is_visible = serializers.BooleanField()
    created_at = serializers.DateTimeField()
    updated_at = serializers.DateTimeField()


class GetProductVariantsOutSerializer(serializers.Serializer):
    count = serializers.IntegerField()
    results = ProductVariantOutSerializer(many=True)

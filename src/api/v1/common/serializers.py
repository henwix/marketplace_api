from django.utils.translation import gettext_lazy as _
from rest_framework import serializers


class DetailOutSerializer(serializers.Serializer):
    detail = serializers.CharField(max_length=255, help_text=_('Detailed response message'))


class BaseInSerializer(serializers.Serializer):
    @classmethod
    def validate_data(cls, data: dict, raise_exception: bool = True, partial: bool = False) -> dict:
        serializer = cls(data=data, partial=partial)
        serializer.is_valid(raise_exception=raise_exception)
        return serializer.validated_data

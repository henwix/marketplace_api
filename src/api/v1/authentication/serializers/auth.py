from django.utils.translation import gettext_lazy as _
from rest_framework import serializers


class DetailTokenOutSerializer(serializers.Serializer):
    detail = serializers.CharField(max_length=255, help_text=_('Detailed response message'))
    code = serializers.CharField(max_length=255, help_text=_('Error code'))
    messages = serializers.ListField(help_text=_('Messages list'))

from rest_framework import serializers


class DetailOutSerializer(serializers.Serializer):
    detail = serializers.CharField(max_length=255, help_text='Detailed response message')

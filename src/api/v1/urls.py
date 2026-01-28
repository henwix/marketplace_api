from django.urls import include, path
from drf_spectacular.utils import extend_schema, inline_serializer
from rest_framework import serializers
from rest_framework.decorators import api_view
from rest_framework.request import Request
from rest_framework.views import Response

app_name = 'v1'


@extend_schema(
    responses=inline_serializer(name='ping', fields={'detail': serializers.CharField(default='pong')}),
    summary='Ping API GET',
)
@api_view(['GET'])
def ping(request: Request) -> Response:
    return Response({'detail': 'pong'})


urlpatterns = [
    path('ping/', ping, name='ping'),
    path('', include('src.api.v1.users.urls')),
    path('', include('src.api.v1.sellers.urls')),
    path('', include('src.api.v1.products.urls')),
    path('', include('src.api.v1.cart.urls')),
    path('', include('src.api.v1.authentication.urls')),
]

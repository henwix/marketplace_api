from django.urls import include, path
from rest_framework.decorators import api_view
from rest_framework.views import Response

app_name = 'v1'


@api_view(['GET'])
def ping(request):
    return Response({'detail': 'pong'})


urlpatterns = [
    path('ping/', ping, name='ping'),
    path('', include('src.api.v1.users.urls')),
]

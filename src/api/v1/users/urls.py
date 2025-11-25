from django.urls import include, path

from src.api.v1.users.views import UserViewSet
from src.apps.users.routers import CustomUserRouter

app_name = 'users'


user_router = CustomUserRouter()
user_router.register(prefix='users', viewset=UserViewSet, basename='users')


urlpatterns = [
    path('', include(user_router.urls)),
]

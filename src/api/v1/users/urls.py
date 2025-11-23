from django.urls import include, path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView

from src.api.v1.users.views import UserViewSet
from src.apps.users.routers import CustomUserRouter

app_name = 'users'


user_router = CustomUserRouter()
user_router.register(prefix='users', viewset=UserViewSet, basename='users')


urlpatterns = [
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('', include(user_router.urls)),
]

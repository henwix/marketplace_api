from django.urls import path

from src.api.v1.authentication.views import CustomTokenObtainPairView, CustomTokenRefreshView, CustomTokenVerifyView

app_name = 'auth'


urlpatterns = [
    path('auth/token/', CustomTokenObtainPairView.as_view(), name='token-obtain-pair'),
    path('auth/token_refresh/', CustomTokenRefreshView.as_view(), name='token-refresh'),
    path('auth/token_verify/', CustomTokenVerifyView.as_view(), name='token-verify'),
]

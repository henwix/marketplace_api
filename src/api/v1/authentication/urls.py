from django.urls import path

from src.api.v1.authentication.views.auth import (
    CustomTokenObtainPairView,
    CustomTokenRefreshView,
    CustomTokenVerifyView,
)
from src.api.v1.authentication.views.auth_providers import AuthProviderView
from src.api.v1.authentication.views.oauth import (
    OAuthGetLoginUrlView,
    OAuthVerifyView,
)

app_name = 'auth'


urlpatterns = [
    path('auth/token/', CustomTokenObtainPairView.as_view(), name='auth-token-obtain-pair'),
    path('auth/token_refresh/', CustomTokenRefreshView.as_view(), name='auth-token-refresh'),
    path('auth/token_verify/', CustomTokenVerifyView.as_view(), name='auth-token-verify'),
    path('auth/providers/', AuthProviderView.as_view(), name='auth-providers'),
    path('oauth/login_url/', OAuthGetLoginUrlView.as_view(), name='oauth-login-url'),
    path('oauth/verify/', OAuthVerifyView.as_view(), name='oauth-verify'),
]

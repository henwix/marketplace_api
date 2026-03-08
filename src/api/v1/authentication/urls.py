from django.urls import path

from src.api.v1.authentication.views.authentication import (
    CustomTokenObtainPairView,
    CustomTokenRefreshView,
    CustomTokenVerifyView,
)
from src.api.v1.authentication.views.oauth import OAuthGitHubGetUrlView, OAuthGitHubVerifyView

app_name = 'auth'


urlpatterns = [
    path('auth/token/', CustomTokenObtainPairView.as_view(), name='token-obtain-pair'),
    path('auth/token_refresh/', CustomTokenRefreshView.as_view(), name='token-refresh'),
    path('auth/token_verify/', CustomTokenVerifyView.as_view(), name='token-verify'),
    path('oauth/url/github/', OAuthGitHubGetUrlView.as_view(), name='oauth-github-url'),
    path('oauth/verify/github/', OAuthGitHubVerifyView.as_view(), name='oauth-github-verify'),
]

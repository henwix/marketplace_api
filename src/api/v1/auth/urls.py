from django.urls import path

from src.api.v1.auth.views import CustomTokenObtainPairView, CustomTokenRefreshView, CustomTokenVerifyView

app_name = 'auth'


urlpatterns = [
    path('auth/token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/token_refresh/', CustomTokenRefreshView.as_view(), name='token_refresh'),
    path('auth/token_verify/', CustomTokenVerifyView.as_view(), name='token_verify'),
]

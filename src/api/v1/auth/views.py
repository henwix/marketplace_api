from drf_spectacular.utils import extend_schema
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView


@extend_schema(summary='Generate JWT tokens')
class CustomTokenObtainPairView(TokenObtainPairView): ...


@extend_schema(summary='Refresh JWT token')
class CustomTokenRefreshView(TokenRefreshView): ...


@extend_schema(summary='Verify JWT token')
class CustomTokenVerifyView(TokenVerifyView): ...

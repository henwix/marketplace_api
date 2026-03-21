from drf_spectacular.utils import extend_schema, extend_schema_view

from src.api.v1.authentication.serializers.oauth import OAuthVerifyInSerializer
from src.api.v1.common.openapi.parameters import build_enum_query_parameter
from src.apps.authentication.constants import SocialAccountProviders


def extend_oauth_get_login_url_view_schema(view):
    decorator = extend_schema_view(
        get=extend_schema(
            parameters=[
                build_enum_query_parameter(
                    name='provider',
                    enum=SocialAccountProviders,
                    type=str,
                    required=True,
                )
            ],
            summary='Get OAuth Login URL GET',
        ),
    )
    return decorator(view)


def extend_oauth_verify_view_schema(view):
    decorator = extend_schema_view(
        post=extend_schema(
            request=OAuthVerifyInSerializer,
            summary='Verify OAuth POST',
        ),
    )
    return decorator(view)

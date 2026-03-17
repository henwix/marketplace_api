from drf_spectacular.utils import extend_schema, extend_schema_view

from src.api.v1.authentication.serializers.oauth import OAuthVerifyInSerializer
from src.api.v1.common.openapi.parameters import query_parameter


def extend_oauth_get_login_url_view_schema(view):
    decorator = extend_schema_view(
        get=extend_schema(
            parameters=[
                query_parameter(name='provider', type=str, required=True),
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

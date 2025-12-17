from drf_spectacular.utils import OpenApiParameter


def jwt_header_request_parameter() -> OpenApiParameter:
    return OpenApiParameter(
        name='Authorization',
        type=str,
        location=OpenApiParameter.HEADER,
        required=False,
        description='JWT access token: Bearer <token>',
    )

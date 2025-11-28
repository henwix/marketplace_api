from drf_spectacular.utils import OpenApiParameter

jwt_header_request_parameter = OpenApiParameter(
    name='Authorization',
    type=str,
    location=OpenApiParameter.HEADER,
    required=False,
    description='JWT access token: Bearer <token>',
)

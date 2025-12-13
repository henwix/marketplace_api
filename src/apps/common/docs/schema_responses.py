from drf_spectacular.utils import OpenApiResponse

from src.api.v1.common.serializers import DetailOutSerializer
from src.apps.common.docs.schema_examples import (
    not_found_query_error_404_response_example,
    permission_error_403_response_example,
    unauthorized_error_401_response_example,
)

no_content_204_response = OpenApiResponse(
    description='No response body',
)


unauthorized_error_401_response = OpenApiResponse(
    response=DetailOutSerializer,
    description='Unauthorized error',
    examples=[unauthorized_error_401_response_example],
)


permission_error_403_response = OpenApiResponse(
    response=DetailOutSerializer,
    description='Permission error',
    examples=[permission_error_403_response_example],
)


def not_found_query_error_404_response(object_name: str) -> OpenApiResponse:
    return OpenApiResponse(
        response=DetailOutSerializer,
        description='Not found error',
        examples=[not_found_query_error_404_response_example(object_name=object_name)],
    )

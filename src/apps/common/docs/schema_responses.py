from drf_spectacular.utils import OpenApiResponse

from src.api.v1.common.serializers import DetailOutSerializer
from src.apps.common.docs.schema_examples import (
    permission_error_response_example,
    unauthorized_error_response_example,
)

unauthorized_error_401_response = OpenApiResponse(
    response=DetailOutSerializer,
    description='Unauthorized error',
    examples=[unauthorized_error_response_example],
)


permission_error_403_response = OpenApiResponse(
    response=DetailOutSerializer,
    description='Permission error',
    examples=[permission_error_response_example],
)


no_content_204_response = OpenApiResponse(
    description='No response body',
)

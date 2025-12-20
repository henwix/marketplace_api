from drf_spectacular.utils import OpenApiResponse

from src.api.v1.common.serializers import DetailOutSerializer
from src.apps.common.docs.schema_examples import build_response_example_from_error
from src.apps.products.exceptions.product_variants import ProductVariantNotFoundError


def product_variant_not_found_error_404_response() -> OpenApiResponse:
    return OpenApiResponse(
        response=DetailOutSerializer,
        description='Product variant not found error',
        examples=[
            build_response_example_from_error(ProductVariantNotFoundError),
        ],
    )

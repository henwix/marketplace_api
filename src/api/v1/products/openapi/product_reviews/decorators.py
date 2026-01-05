from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import status

from src.api.v1.common.openapi.responses import successful_response
from src.api.v1.products.serializers.product_reviews import ProductReviewSerializer


def extend_product_review_view_schema():
    return extend_schema_view(
        post=extend_schema(
            request=ProductReviewSerializer,
            responses={
                status.HTTP_201_CREATED: successful_response(response=ProductReviewSerializer),
            },
            summary='Create Product Review POST',
        ),
    )


def extend_detail_product_review_view_schema():
    def _extend_update_product_review_schema(method: str):
        return extend_schema(
            request=ProductReviewSerializer,
            responses={
                status.HTTP_200_OK: successful_response(response=ProductReviewSerializer),
            },
            summary=f'Update Product Review {method}',
        )

    return extend_schema_view(
        delete=extend_schema(
            request=None,
            responses={
                status.HTTP_204_NO_CONTENT: None,
            },
            summary='Delete Product Review DELETE',
        ),
        put=_extend_update_product_review_schema(method='PUT'),
        patch=_extend_update_product_review_schema(method='PATCH'),
    )

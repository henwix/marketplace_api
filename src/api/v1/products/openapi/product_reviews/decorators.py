from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import status

from src.api.v1.authentication.openapi.responses import unauthorized_user_response
from src.api.v1.common.openapi.parameters import (
    jwt_header_parameter,
    ordering_query_parameter,
    page_query_parameter,
    page_size_query_parameter,
)
from src.api.v1.common.openapi.responses import (
    bad_request_response,
    forbidden_response,
    not_found_response,
    successful_page_response,
    successful_response,
)
from src.api.v1.products.openapi.product_reviews.enums import GetProductReviewsOrderingEnum
from src.api.v1.products.pagination import ProductReviewPagination
from src.api.v1.products.serializers.product_reviews import ProductReviewSerializer, RetrieveProductReviewSerializer
from src.apps.products.exceptions.product_reviews import ProductReviewAlreadyExistsError, ProductReviewNotFoundError
from src.apps.products.exceptions.products import ProductNotFoundByIdError
from src.apps.users.exceptions.users import UserNotActiveError, UserNotFoundError


def extend_product_review_view_schema(view):
    def _extend_update_product_review_schema(method: str):
        return extend_schema(
            parameters=[jwt_header_parameter()],
            request=ProductReviewSerializer,
            responses={
                status.HTTP_200_OK: successful_response(response=ProductReviewSerializer),
                status.HTTP_401_UNAUTHORIZED: unauthorized_user_response(),
                status.HTTP_403_FORBIDDEN: forbidden_response(UserNotActiveError),
                status.HTTP_404_NOT_FOUND: not_found_response(
                    UserNotFoundError,
                    ProductNotFoundByIdError,
                    ProductReviewNotFoundError,
                ),
            },
            summary=f'Update Product Review {method}',
        )

    decorator = extend_schema_view(
        post=extend_schema(
            parameters=[jwt_header_parameter()],
            request=ProductReviewSerializer,
            responses={
                status.HTTP_201_CREATED: successful_response(response=ProductReviewSerializer),
                status.HTTP_400_BAD_REQUEST: bad_request_response(ProductReviewAlreadyExistsError),
                status.HTTP_401_UNAUTHORIZED: unauthorized_user_response(),
                status.HTTP_403_FORBIDDEN: forbidden_response(UserNotActiveError),
                status.HTTP_404_NOT_FOUND: not_found_response(
                    UserNotFoundError,
                    ProductNotFoundByIdError,
                ),
            },
            summary='Create Product Review POST',
        ),
        get=extend_schema(
            parameters=[
                ordering_query_parameter(enum=GetProductReviewsOrderingEnum),
                page_query_parameter(paginator=ProductReviewPagination),
                page_size_query_parameter(paginator=ProductReviewPagination),
            ],
            request=None,
            responses={
                status.HTTP_200_OK: successful_page_response(
                    response=RetrieveProductReviewSerializer,
                    paginator=ProductReviewPagination,
                ),
                status.HTTP_404_NOT_FOUND: not_found_response(ProductNotFoundByIdError),
            },
            summary='Get Product Reviews GET',
        ),
        delete=extend_schema(
            parameters=[jwt_header_parameter()],
            request=None,
            responses={
                status.HTTP_204_NO_CONTENT: None,
                status.HTTP_401_UNAUTHORIZED: unauthorized_user_response(),
                status.HTTP_403_FORBIDDEN: forbidden_response(UserNotActiveError),
                status.HTTP_404_NOT_FOUND: not_found_response(
                    UserNotFoundError,
                    ProductNotFoundByIdError,
                    ProductReviewNotFoundError,
                ),
            },
            summary='Delete Product Review DELETE',
        ),
        put=_extend_update_product_review_schema(method='PUT'),
        patch=_extend_update_product_review_schema(method='PATCH'),
    )
    return decorator(view)

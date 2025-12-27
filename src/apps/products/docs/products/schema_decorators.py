from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import OpenApiParameter, extend_schema, extend_schema_view
from rest_framework import status

from src.api.v1.products.serializers.products import (
    ProductSerializer,
    RetrieveProductSerializer,
    SearchProductSerializer,
)
from src.apps.authentication.docs.schema_responses import unauthorized_user_response
from src.apps.common.docs.schema_parameters import build_enum_query_param, jwt_header_request_parameter
from src.apps.common.docs.schema_responses import (
    forbidden_response,
    not_found_response,
    permission_error_403_response,
    successful_response,
    unauthorized_error_401_response,
)
from src.apps.products.docs.products.enums import ProductsSearchOrderingEnum
from src.apps.products.exceptions.products import (
    ProductAccessForbiddenError,
    ProductNotFoundByIdError,
    ProductNotFoundBySlugError,
)
from src.apps.sellers.exceptions import SellerNotFoundError
from src.apps.users.exceptions.users import UserNotActiveError, UserNotFoundError


def extend_product_view_schema():
    return extend_schema_view(
        post=extend_schema(
            parameters=[jwt_header_request_parameter()],
            request=ProductSerializer,
            responses={
                status.HTTP_201_CREATED: successful_response(response=ProductSerializer),
                status.HTTP_401_UNAUTHORIZED: unauthorized_user_response(),
                status.HTTP_403_FORBIDDEN: forbidden_response(UserNotActiveError),
                status.HTTP_404_NOT_FOUND: not_found_response(SellerNotFoundError, UserNotFoundError),
            },
            summary='Create Product POST',
        )
    )


def extend_detail_slug_product_view_schema():
    return extend_schema_view(
        get=extend_schema(
            parameters=[jwt_header_request_parameter()],
            request=None,
            responses={
                status.HTTP_200_OK: successful_response(response=RetrieveProductSerializer),
                status.HTTP_401_UNAUTHORIZED: unauthorized_user_response(include_credentials_error=False),
                status.HTTP_403_FORBIDDEN: forbidden_response(ProductAccessForbiddenError, UserNotActiveError),
                status.HTTP_404_NOT_FOUND: not_found_response(ProductNotFoundBySlugError, UserNotFoundError),
            },
            summary='Retrieve Product By Slug GET',
        )
    )


def extend_detail_product_view_schema():
    def _update_product_extend_schema(method: str):
        return extend_schema(
            parameters=[jwt_header_request_parameter()],
            request=ProductSerializer,
            responses={
                status.HTTP_200_OK: successful_response(response=ProductSerializer),
                status.HTTP_401_UNAUTHORIZED: unauthorized_user_response(),
                status.HTTP_403_FORBIDDEN: forbidden_response(ProductAccessForbiddenError, UserNotActiveError),
                status.HTTP_404_NOT_FOUND: not_found_response(
                    SellerNotFoundError, ProductNotFoundByIdError, UserNotFoundError
                ),
            },
            summary=f'Update Product {method}',
        )

    return extend_schema_view(
        get=extend_schema(
            parameters=[jwt_header_request_parameter()],
            request=None,
            responses={
                status.HTTP_200_OK: successful_response(response=RetrieveProductSerializer),
                status.HTTP_401_UNAUTHORIZED: unauthorized_user_response(include_credentials_error=False),
                status.HTTP_403_FORBIDDEN: forbidden_response(ProductAccessForbiddenError, UserNotActiveError),
                status.HTTP_404_NOT_FOUND: not_found_response(ProductNotFoundByIdError, UserNotFoundError),
            },
            summary='Retrieve Product By Id GET',
        ),
        delete=extend_schema(
            parameters=[jwt_header_request_parameter()],
            request=None,
            responses={
                status.HTTP_204_NO_CONTENT: None,
                status.HTTP_401_UNAUTHORIZED: unauthorized_user_response(),
                status.HTTP_403_FORBIDDEN: forbidden_response(ProductAccessForbiddenError, UserNotActiveError),
                status.HTTP_404_NOT_FOUND: not_found_response(
                    SellerNotFoundError, ProductNotFoundByIdError, UserNotFoundError
                ),
            },
            summary='Delete Product DELETE',
        ),
        put=_update_product_extend_schema(method='PUT'),
        patch=_update_product_extend_schema(method='PATCH'),
    )


def extend_global_search_view_schema():
    return extend_schema(
        parameters=[
            build_enum_query_param(
                name='o', enum=ProductsSearchOrderingEnum, description='Which field to use when ordering the results.'
            ),
            OpenApiParameter(name='max_price', description='Maximum price', type=OpenApiTypes.DECIMAL),
            OpenApiParameter(name='min_price', description='Minimum price', type=OpenApiTypes.DECIMAL),
            OpenApiParameter(name='price_range_max', description='Price range', type=OpenApiTypes.DECIMAL),
            OpenApiParameter(name='price_range_min', description='Price range', type=OpenApiTypes.DECIMAL),
        ],
        request=None,
        responses={
            status.HTTP_200_OK: successful_response(response=SearchProductSerializer),
        },
        summary='Search Global Products GET',
    )


def extend_personal_search_view_schema():
    return extend_schema(
        parameters=[
            jwt_header_request_parameter(),
            build_enum_query_param(
                name='o', enum=ProductsSearchOrderingEnum, description='Which field to use when ordering the results.'
            ),
            OpenApiParameter(name='is_visible', description='Is visible', type=OpenApiTypes.BOOL),
            OpenApiParameter(name='max_price', description='Maximum price', type=OpenApiTypes.DECIMAL),
            OpenApiParameter(name='min_price', description='Minimum price', type=OpenApiTypes.DECIMAL),
            OpenApiParameter(name='price_range_max', description='Price range', type=OpenApiTypes.DECIMAL),
            OpenApiParameter(name='price_range_min', description='Price range', type=OpenApiTypes.DECIMAL),
        ],
        request=None,
        responses={
            status.HTTP_200_OK: successful_response(response=SearchProductSerializer),
            status.HTTP_401_UNAUTHORIZED: unauthorized_error_401_response(),
            status.HTTP_403_FORBIDDEN: permission_error_403_response(),
        },
        summary='Search Personal Products GET',
    )

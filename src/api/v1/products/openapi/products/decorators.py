from decimal import Decimal

from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import status

from src.api.v1.authentication.openapi.responses import unauthorized_user_response
from src.api.v1.common.openapi.parameters import (
    jwt_header_parameter,
    ordering_query_parameter,
    page_query_parameter,
    page_size_query_parameter,
    query_parameter,
    search_query_parameter,
)
from src.api.v1.common.openapi.responses import (
    forbidden_response,
    not_found_response,
    successful_page_response,
    successful_response,
)
from src.api.v1.products.openapi.products.enums import ProductsSearchOrderingEnum
from src.api.v1.products.pagination import SearchProductPagination
from src.api.v1.products.serializers.products import (
    ProductSerializer,
    RetrieveProductSerializer,
    SearchProductSerializer,
)
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
            parameters=[jwt_header_parameter()],
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
            parameters=[jwt_header_parameter()],
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
            parameters=[jwt_header_parameter()],
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
            parameters=[jwt_header_parameter()],
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
            parameters=[jwt_header_parameter()],
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
            search_query_parameter(),
            ordering_query_parameter(enum=ProductsSearchOrderingEnum),
            page_query_parameter(paginator=SearchProductPagination),
            page_size_query_parameter(paginator=SearchProductPagination),
            query_parameter(name='max_price', type=Decimal, description='Maximum price'),
            query_parameter(name='min_price', type=Decimal, description='Minimum price'),
            query_parameter(name='price_range_max', type=Decimal, description='Price range'),
            query_parameter(name='price_range_min', type=Decimal, description='Price range'),
        ],
        request=None,
        responses={
            status.HTTP_200_OK: successful_page_response(
                response=SearchProductSerializer,
                paginator=SearchProductPagination,
            ),
        },
        summary='Search Global Products GET',
    )


def extend_personal_search_view_schema():
    return extend_schema(
        parameters=[
            jwt_header_parameter(),
            search_query_parameter(),
            ordering_query_parameter(enum=ProductsSearchOrderingEnum),
            page_query_parameter(paginator=SearchProductPagination),
            page_size_query_parameter(paginator=SearchProductPagination),
            query_parameter(name='is_visible', type=bool, description='Is visible'),
            query_parameter(name='max_price', type=Decimal, description='Maximum price'),
            query_parameter(name='min_price', type=Decimal, description='Minimum price'),
            query_parameter(name='price_range_max', type=Decimal, description='Price range'),
            query_parameter(name='price_range_min', type=Decimal, description='Price range'),
        ],
        request=None,
        responses={
            status.HTTP_200_OK: successful_page_response(
                response=SearchProductSerializer,
                paginator=SearchProductPagination,
            ),
            status.HTTP_401_UNAUTHORIZED: unauthorized_user_response(),
            status.HTTP_403_FORBIDDEN: forbidden_response(UserNotActiveError),
            status.HTTP_404_NOT_FOUND: not_found_response(SellerNotFoundError, UserNotFoundError),
        },
        summary='Search Personal Products GET',
    )

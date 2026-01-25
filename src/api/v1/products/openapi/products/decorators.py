from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import status

from src.api.v1.authentication.openapi.responses import unauthorized_user_response
from src.api.v1.common.openapi.parameters import (
    cursor_query_parameter,
    jwt_header_parameter,
    ordering_query_parameter,
    page_query_parameter,
    page_size_query_parameter,
    query_parameter,
    search_query_parameter,
)
from src.api.v1.common.openapi.responses import (
    bad_request_response,
    forbidden_response,
    not_found_response,
    successful_cursor_response,
    successful_page_response,
    successful_response,
)
from src.api.v1.products.openapi.products.enums import (
    ProductsGlobalSearchOrderingEnum,
    ProductsPersonalSearchOrderingEnum,
)
from src.api.v1.products.pagination import SearchProductCursorPagination, SearchProductPagePagination
from src.api.v1.products.serializers.products import (
    CreateProductInSerializer,
    ProductOutSerializer,
    RetrieveProductOutSerializer,
    SearchProductOutSerializer,
    UpdateProductInSerializer,
)
from src.apps.common.exceptions import NothingToUpdateError
from src.apps.products.exceptions.products import (
    ProductAccessForbiddenError,
    ProductNotFoundByIdError,
    ProductNotFoundBySlugError,
)
from src.apps.sellers.exceptions import SellerNotFoundError
from src.apps.users.exceptions.users import UserNotActiveError, UserNotFoundError


def extend_product_view_schema(view):
    decorator = extend_schema_view(
        post=extend_schema(
            parameters=[jwt_header_parameter()],
            request=CreateProductInSerializer,
            responses={
                status.HTTP_201_CREATED: successful_response(response=ProductOutSerializer),
                status.HTTP_401_UNAUTHORIZED: unauthorized_user_response(),
                status.HTTP_403_FORBIDDEN: forbidden_response(UserNotActiveError),
                status.HTTP_404_NOT_FOUND: not_found_response(SellerNotFoundError, UserNotFoundError),
            },
            summary='Create Product POST',
        )
    )
    return decorator(view)


def extend_detail_slug_product_view_schema(view):
    decorator = extend_schema_view(
        get=extend_schema(
            parameters=[jwt_header_parameter()],
            request=None,
            responses={
                status.HTTP_200_OK: successful_response(response=RetrieveProductOutSerializer),
                status.HTTP_401_UNAUTHORIZED: unauthorized_user_response(include_credentials_error=False),
                status.HTTP_403_FORBIDDEN: forbidden_response(ProductAccessForbiddenError, UserNotActiveError),
                status.HTTP_404_NOT_FOUND: not_found_response(ProductNotFoundBySlugError, UserNotFoundError),
            },
            summary='Retrieve Product By Slug GET',
        )
    )
    return decorator(view)


def extend_detail_product_view_schema(view):
    decorator = extend_schema_view(
        get=extend_schema(
            parameters=[jwt_header_parameter()],
            request=None,
            responses={
                status.HTTP_200_OK: successful_response(response=RetrieveProductOutSerializer),
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
        patch=extend_schema(
            parameters=[jwt_header_parameter()],
            request=UpdateProductInSerializer,
            responses={
                status.HTTP_200_OK: successful_response(response=ProductOutSerializer),
                status.HTTP_400_BAD_REQUEST: bad_request_response(NothingToUpdateError),
                status.HTTP_401_UNAUTHORIZED: unauthorized_user_response(),
                status.HTTP_403_FORBIDDEN: forbidden_response(ProductAccessForbiddenError, UserNotActiveError),
                status.HTTP_404_NOT_FOUND: not_found_response(
                    SellerNotFoundError, ProductNotFoundByIdError, UserNotFoundError
                ),
            },
            summary='Update Product PATCH',
        ),
        put=extend_schema(
            parameters=[jwt_header_parameter()],
            request=UpdateProductInSerializer,
            responses={
                status.HTTP_200_OK: successful_response(response=ProductOutSerializer),
                status.HTTP_401_UNAUTHORIZED: unauthorized_user_response(),
                status.HTTP_403_FORBIDDEN: forbidden_response(ProductAccessForbiddenError, UserNotActiveError),
                status.HTTP_404_NOT_FOUND: not_found_response(
                    SellerNotFoundError, ProductNotFoundByIdError, UserNotFoundError
                ),
            },
            summary='Update Product PUT',
        ),
    )
    return decorator(view)


def extend_global_search_view_schema(view):
    decorator = extend_schema(
        parameters=[
            search_query_parameter(),
            ordering_query_parameter(enum=ProductsGlobalSearchOrderingEnum),
            cursor_query_parameter(paginator=SearchProductCursorPagination),
            page_size_query_parameter(paginator=SearchProductCursorPagination),
        ],
        request=None,
        responses={
            status.HTTP_200_OK: successful_cursor_response(
                response=SearchProductOutSerializer,
                paginator=SearchProductCursorPagination,
            ),
        },
        summary='Search Global Products GET',
    )
    return decorator(view)


def extend_personal_search_view_schema(view):
    decorator = extend_schema(
        parameters=[
            jwt_header_parameter(),
            search_query_parameter(),
            ordering_query_parameter(enum=ProductsPersonalSearchOrderingEnum),
            page_query_parameter(paginator=SearchProductPagePagination),
            page_size_query_parameter(paginator=SearchProductPagePagination),
            query_parameter(name='is_visible', type=bool, description='Is visible'),
        ],
        request=None,
        responses={
            status.HTTP_200_OK: successful_page_response(
                response=SearchProductOutSerializer,
                paginator=SearchProductPagePagination,
            ),
            status.HTTP_401_UNAUTHORIZED: unauthorized_user_response(),
            status.HTTP_403_FORBIDDEN: forbidden_response(UserNotActiveError),
            status.HTTP_404_NOT_FOUND: not_found_response(SellerNotFoundError, UserNotFoundError),
        },
        summary='Search Personal Products GET',
    )
    return decorator(view)

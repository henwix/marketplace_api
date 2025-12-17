from drf_spectacular.utils import OpenApiResponse, extend_schema, extend_schema_view
from rest_framework import status

from src.api.v1.products.serializers.products import (
    ProductSerializer,
    RetrieveProductSerializer,
    SearchProductSerializer,
)
from src.apps.common.docs.schema_parameters import jwt_header_request_parameter
from src.apps.common.docs.schema_responses import permission_error_403_response, unauthorized_error_401_response
from src.apps.products.docs.products.schema_responses import (
    product_extended_permission_error_403_response,
    product_not_found_error_404_response,
    product_permission_error_403_response,
)


def extend_create_product_view_schema():
    return extend_schema_view(
        post=extend_schema(
            parameters=[jwt_header_request_parameter()],
            request=ProductSerializer,
            responses={
                status.HTTP_201_CREATED: OpenApiResponse(
                    response=ProductSerializer,
                    description='Product has been created',
                ),
                status.HTTP_401_UNAUTHORIZED: unauthorized_error_401_response(),
                status.HTTP_403_FORBIDDEN: permission_error_403_response(),
            },
            summary='Create Product POST',
        )
    )


def extend_get_product_by_slug_view_schema():
    return extend_schema_view(
        get=extend_schema(
            parameters=[jwt_header_request_parameter()],
            request=None,
            responses={
                status.HTTP_200_OK: OpenApiResponse(
                    response=RetrieveProductSerializer,
                    description='Product has been retrieved by slug',
                ),
                status.HTTP_403_FORBIDDEN: product_permission_error_403_response(),
                status.HTTP_404_NOT_FOUND: product_not_found_error_404_response(),
            },
            summary='Retrieve Product By Slug GET',
        )
    )


def _update_product_extend_schema(method: str):
    return extend_schema(
        parameters=[jwt_header_request_parameter()],
        request=ProductSerializer,
        responses={
            status.HTTP_200_OK: ProductSerializer,
            status.HTTP_401_UNAUTHORIZED: unauthorized_error_401_response(),
            status.HTTP_403_FORBIDDEN: product_extended_permission_error_403_response(),
            status.HTTP_404_NOT_FOUND: product_not_found_error_404_response(),
        },
        summary=f'Update Product {method}',
    )


def extend_detail_product_view_schema():
    return extend_schema_view(
        get=extend_schema(
            parameters=[jwt_header_request_parameter()],
            request=None,
            responses={
                status.HTTP_200_OK: OpenApiResponse(
                    response=RetrieveProductSerializer,
                    description='Product has been retrieved by id',
                ),
                status.HTTP_403_FORBIDDEN: product_permission_error_403_response(),
                status.HTTP_404_NOT_FOUND: product_not_found_error_404_response(),
            },
            summary='Retrieve Product By Id GET',
        ),
        delete=extend_schema(
            parameters=[jwt_header_request_parameter()],
            request=None,
            responses={
                status.HTTP_204_NO_CONTENT: None,
                status.HTTP_401_UNAUTHORIZED: unauthorized_error_401_response(),
                status.HTTP_403_FORBIDDEN: product_extended_permission_error_403_response(),
                status.HTTP_404_NOT_FOUND: product_not_found_error_404_response(),
            },
            summary='Delete Product DELETE',
        ),
        put=_update_product_extend_schema(method='PUT'),
        patch=_update_product_extend_schema(method='PATCH'),
    )


def extend_global_search_view_schema():
    return extend_schema(
        request=None,
        responses={
            status.HTTP_200_OK: OpenApiResponse(
                response=SearchProductSerializer,
                description='Global products were found',
            ),
        },
        summary='Search Global Products GET',
    )


def extend_personal_search_view_schema():
    return extend_schema(
        parameters=[jwt_header_request_parameter()],
        request=None,
        responses={
            status.HTTP_200_OK: OpenApiResponse(
                response=SearchProductSerializer,
                description='Personal products were found',
            ),
            status.HTTP_401_UNAUTHORIZED: unauthorized_error_401_response(),
            status.HTTP_403_FORBIDDEN: permission_error_403_response(),
        },
        summary='Search Personal Products GET',
    )

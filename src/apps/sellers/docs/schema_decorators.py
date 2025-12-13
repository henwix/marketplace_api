from drf_spectacular.utils import OpenApiResponse, extend_schema, extend_schema_view
from rest_framework import status

from src.api.v1.sellers.serializers import SellerSerializer
from src.apps.common.docs.schema_parameters import jwt_header_request_parameter
from src.apps.common.docs.schema_responses import (
    no_content_204_response,
    permission_error_403_response,
    unauthorized_error_401_response,
)

extend_seller_viewset_schema = extend_schema_view(
    create=extend_schema(
        parameters=[jwt_header_request_parameter],
        request=SellerSerializer,
        responses={
            status.HTTP_201_CREATED: OpenApiResponse(
                response=SellerSerializer,
                description='Seller profile has been created',
            ),
            status.HTTP_401_UNAUTHORIZED: unauthorized_error_401_response,
            status.HTTP_403_FORBIDDEN: permission_error_403_response,
        },
        summary='Create Seller Profile POST',
    ),
    retrieve=extend_schema(
        parameters=[jwt_header_request_parameter],
        responses={
            status.HTTP_200_OK: OpenApiResponse(
                response=SellerSerializer,
                description='Seller profile has been retrieved',
            ),
            status.HTTP_401_UNAUTHORIZED: unauthorized_error_401_response,
            status.HTTP_403_FORBIDDEN: permission_error_403_response,
        },
        summary='Retrieve Seller Profile GET',
    ),
    update=extend_schema(
        parameters=[jwt_header_request_parameter],
        responses={
            status.HTTP_200_OK: OpenApiResponse(
                response=SellerSerializer, description='Seller profile has been updated'
            ),
            status.HTTP_401_UNAUTHORIZED: unauthorized_error_401_response,
            status.HTTP_403_FORBIDDEN: permission_error_403_response,
        },
        summary='Update Seller Profile PUT',
    ),
    partial_update=extend_schema(
        parameters=[jwt_header_request_parameter],
        responses={
            status.HTTP_200_OK: OpenApiResponse(
                response=SellerSerializer, description='Seller profile has been updated'
            ),
            status.HTTP_401_UNAUTHORIZED: unauthorized_error_401_response,
            status.HTTP_403_FORBIDDEN: permission_error_403_response,
        },
        summary='Update Seller Profile PATCH',
    ),
    destroy=extend_schema(
        parameters=[jwt_header_request_parameter],
        responses={
            status.HTTP_204_NO_CONTENT: no_content_204_response,
            status.HTTP_401_UNAUTHORIZED: unauthorized_error_401_response,
            status.HTTP_403_FORBIDDEN: permission_error_403_response,
        },
        summary='Delete Seller Profile DELETE',
    ),
)

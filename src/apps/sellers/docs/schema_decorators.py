from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import status

from src.api.v1.sellers.serializers import SellerSerializer
from src.apps.common.docs.schema_parameters import jwt_header_request_parameter
from src.apps.common.docs.schema_responses import (
    bad_request_error_response,
    not_found_error_response,
    successful_response,
)
from src.apps.sellers.exceptions import SellerAlreadyExistsError, SellerNotFoundByIdError, SellerNotFoundError
from src.apps.users.docs.schema_responses import (
    unauthorized_user_response,
)


def _update_seller_extend_schema(method: str):
    return (
        extend_schema(
            parameters=[jwt_header_request_parameter()],
            request=SellerSerializer,
            responses={
                status.HTTP_200_OK: successful_response(response=SellerSerializer),
                status.HTTP_401_UNAUTHORIZED: unauthorized_user_response(),
                status.HTTP_404_NOT_FOUND: not_found_error_response(SellerNotFoundError),
            },
            summary=f'Update Seller Profile {method}',
        ),
    )


def extend_seller_view_schema():
    return extend_schema_view(
        post=extend_schema(
            parameters=[jwt_header_request_parameter()],
            request=SellerSerializer,
            responses={
                status.HTTP_201_CREATED: successful_response(response=SellerSerializer),
                status.HTTP_400_BAD_REQUEST: bad_request_error_response(SellerAlreadyExistsError),
                status.HTTP_401_UNAUTHORIZED: unauthorized_user_response(),
            },
            summary='Create Seller Profile POST',
        ),
        get=extend_schema(
            parameters=[jwt_header_request_parameter()],
            responses={
                status.HTTP_200_OK: successful_response(response=SellerSerializer),
                status.HTTP_401_UNAUTHORIZED: unauthorized_user_response(),
                status.HTTP_404_NOT_FOUND: not_found_error_response(SellerNotFoundError),
            },
            summary='Retrieve Seller Profile GET',
        ),
        put=_update_seller_extend_schema(method='PUT'),
        patch=_update_seller_extend_schema(method='PATCH'),
        delete=extend_schema(
            parameters=[jwt_header_request_parameter()],
            responses={
                status.HTTP_204_NO_CONTENT: None,
                status.HTTP_401_UNAUTHORIZED: unauthorized_user_response(),
                status.HTTP_404_NOT_FOUND: not_found_error_response(SellerNotFoundError),
            },
            summary='Delete Seller Profile DELETE',
        ),
    )


def extend_detail_seller_view_schema():
    return extend_schema_view(
        get=extend_schema(
            responses={
                status.HTTP_200_OK: successful_response(response=SellerSerializer),
                status.HTTP_404_NOT_FOUND: not_found_error_response(SellerNotFoundByIdError),
            },
            summary='Retrieve Seller Profile By Id GET',
        ),
    )

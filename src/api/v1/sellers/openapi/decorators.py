from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import status

from src.api.v1.authentication.openapi.responses import unauthorized_user_response
from src.api.v1.common.openapi.parameters import jwt_header_parameter
from src.api.v1.common.openapi.responses import (
    bad_request_response,
    forbidden_response,
    not_found_response,
    successful_response,
)
from src.api.v1.sellers.serializers import CreateSellerInSerializer, SellerOutSerializer, UpdateSellerInSerializer
from src.apps.common.exceptions import NothingToUpdateError
from src.apps.sellers.exceptions import SellerAlreadyExistsError, SellerNotFoundByIdError, SellerNotFoundError
from src.apps.users.exceptions.users import UserNotActiveError, UserNotFoundError


def extend_seller_view_schema(view):
    def _update_seller_extend_schema(method: str):
        return extend_schema(
            parameters=[jwt_header_parameter()],
            request=UpdateSellerInSerializer,
            responses={
                status.HTTP_200_OK: successful_response(response=SellerOutSerializer),
                status.HTTP_400_BAD_REQUEST: bad_request_response(NothingToUpdateError),
                status.HTTP_401_UNAUTHORIZED: unauthorized_user_response(),
                status.HTTP_403_FORBIDDEN: forbidden_response(UserNotActiveError),
                status.HTTP_404_NOT_FOUND: not_found_response(SellerNotFoundError, UserNotFoundError),
            },
            summary=f'Update Seller Profile {method}',
        )

    decorator = extend_schema_view(
        post=extend_schema(
            parameters=[jwt_header_parameter()],
            request=CreateSellerInSerializer,
            responses={
                status.HTTP_201_CREATED: successful_response(response=SellerOutSerializer),
                status.HTTP_400_BAD_REQUEST: bad_request_response(SellerAlreadyExistsError),
                status.HTTP_401_UNAUTHORIZED: unauthorized_user_response(),
                status.HTTP_403_FORBIDDEN: forbidden_response(UserNotActiveError),
                status.HTTP_404_NOT_FOUND: not_found_response(UserNotFoundError),
            },
            summary='Create Seller Profile POST',
        ),
        get=extend_schema(
            parameters=[jwt_header_parameter()],
            responses={
                status.HTTP_200_OK: successful_response(response=SellerOutSerializer),
                status.HTTP_401_UNAUTHORIZED: unauthorized_user_response(),
                status.HTTP_403_FORBIDDEN: forbidden_response(UserNotActiveError),
                status.HTTP_404_NOT_FOUND: not_found_response(SellerNotFoundError, UserNotFoundError),
            },
            summary='Retrieve Seller Profile GET',
        ),
        patch=_update_seller_extend_schema(method='PATCH'),
        put=_update_seller_extend_schema(method='PUT'),
        delete=extend_schema(
            parameters=[jwt_header_parameter()],
            responses={
                status.HTTP_204_NO_CONTENT: None,
                status.HTTP_401_UNAUTHORIZED: unauthorized_user_response(),
                status.HTTP_403_FORBIDDEN: forbidden_response(UserNotActiveError),
                status.HTTP_404_NOT_FOUND: not_found_response(SellerNotFoundError, UserNotFoundError),
            },
            summary='Delete Seller Profile DELETE',
        ),
    )
    return decorator(view)


def extend_detail_seller_view_schema(view):
    decorator = extend_schema_view(
        get=extend_schema(
            responses={
                status.HTTP_200_OK: successful_response(response=SellerOutSerializer),
                status.HTTP_404_NOT_FOUND: not_found_response(SellerNotFoundByIdError),
            },
            summary='Retrieve Seller Profile By Id GET',
        ),
    )
    return decorator(view)

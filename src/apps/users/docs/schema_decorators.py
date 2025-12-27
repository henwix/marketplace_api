from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import status

from src.api.v1.common.serializers import DetailOutSerializer
from src.api.v1.users.serializers import PasswordUserSerializer, UpdateUserSerializer, UserSerializer
from src.apps.authentication.docs.schema_responses import unauthorized_user_response
from src.apps.common.docs.schema_examples import (
    build_detail_response_example,
)
from src.apps.common.docs.schema_parameters import jwt_header_request_parameter
from src.apps.common.docs.schema_responses import (
    bad_request_response,
    forbidden_response,
    not_found_response,
    successful_response,
)
from src.apps.users.exceptions.users import UserNotActiveError, UserNotFoundError, UserWithDataAlreadyExistsError


def extend_user_view_schema():
    def _update_user_extend_schema(method: str):
        return extend_schema(
            parameters=[jwt_header_request_parameter()],
            request=UpdateUserSerializer,
            responses={
                status.HTTP_200_OK: successful_response(response=UpdateUserSerializer),
                status.HTTP_400_BAD_REQUEST: bad_request_response(UserWithDataAlreadyExistsError),
                status.HTTP_401_UNAUTHORIZED: unauthorized_user_response(),
                status.HTTP_403_FORBIDDEN: forbidden_response(UserNotActiveError),
                status.HTTP_404_NOT_FOUND: not_found_response(UserNotFoundError),
            },
            summary=f'Update User {method}',
        )

    return extend_schema_view(
        post=extend_schema(
            request=UserSerializer,
            responses={
                status.HTTP_201_CREATED: successful_response(response=UserSerializer),
                status.HTTP_400_BAD_REQUEST: bad_request_response(UserWithDataAlreadyExistsError),
            },
            summary='Create User POST',
        ),
        get=extend_schema(
            parameters=[jwt_header_request_parameter()],
            request=None,
            responses={
                status.HTTP_200_OK: successful_response(response=UserSerializer),
                status.HTTP_401_UNAUTHORIZED: unauthorized_user_response(),
                status.HTTP_403_FORBIDDEN: forbidden_response(UserNotActiveError),
                status.HTTP_404_NOT_FOUND: not_found_response(UserNotFoundError),
            },
            summary='Retrieve User GET',
        ),
        put=_update_user_extend_schema(method='PUT'),
        patch=_update_user_extend_schema(method='PATCH'),
        delete=extend_schema(
            parameters=[jwt_header_request_parameter()],
            request=None,
            responses={
                status.HTTP_204_NO_CONTENT: None,
                status.HTTP_401_UNAUTHORIZED: unauthorized_user_response(),
                status.HTTP_403_FORBIDDEN: forbidden_response(UserNotActiveError),
                status.HTTP_404_NOT_FOUND: not_found_response(UserNotFoundError),
            },
            summary='Delete User DELETE',
        ),
    )


def extend_set_password_user_view_schema():
    return extend_schema_view(
        post=extend_schema(
            parameters=[jwt_header_request_parameter()],
            request=PasswordUserSerializer,
            responses={
                status.HTTP_200_OK: successful_response(
                    build_detail_response_example(name='Password updated', value='Success', status_code=200),
                    response=DetailOutSerializer,
                ),
                status.HTTP_401_UNAUTHORIZED: unauthorized_user_response(),
                status.HTTP_403_FORBIDDEN: forbidden_response(UserNotActiveError),
                status.HTTP_404_NOT_FOUND: not_found_response(UserNotFoundError),
            },
            summary='Update User Password POST',
        )
    )

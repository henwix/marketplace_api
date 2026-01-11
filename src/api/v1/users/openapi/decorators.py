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
from src.api.v1.users.serializers import (
    CreateUserInSerializer,
    SetPasswordUserInSerializer,
    UpdateUserInSerializer,
    UserOutSerializer,
)
from src.apps.users.exceptions.users import (
    UserNotActiveError,
    UserNotFoundError,
    UserWithDataAlreadyExistsError,
    UserWithEmailAlreadyExistsError,
    UserWithPhoneAlreadyExistsError,
)


def extend_user_view_schema(view):
    decorator = extend_schema_view(
        post=extend_schema(
            request=CreateUserInSerializer,
            responses={
                status.HTTP_201_CREATED: successful_response(response=UserOutSerializer),
                status.HTTP_400_BAD_REQUEST: bad_request_response(
                    UserWithEmailAlreadyExistsError,
                    UserWithPhoneAlreadyExistsError,
                    UserWithDataAlreadyExistsError,
                ),
            },
            summary='Create User POST',
        ),
        get=extend_schema(
            parameters=[jwt_header_parameter()],
            request=None,
            responses={
                status.HTTP_200_OK: successful_response(response=UserOutSerializer),
                status.HTTP_401_UNAUTHORIZED: unauthorized_user_response(),
                status.HTTP_403_FORBIDDEN: forbidden_response(UserNotActiveError),
                status.HTTP_404_NOT_FOUND: not_found_response(UserNotFoundError),
            },
            summary='Retrieve User GET',
        ),
        patch=extend_schema(
            parameters=[jwt_header_parameter()],
            request=UpdateUserInSerializer,
            responses={
                status.HTTP_200_OK: successful_response(response=UserOutSerializer),
                status.HTTP_400_BAD_REQUEST: bad_request_response(
                    UserWithEmailAlreadyExistsError,
                    UserWithPhoneAlreadyExistsError,
                    UserWithDataAlreadyExistsError,
                ),
                status.HTTP_401_UNAUTHORIZED: unauthorized_user_response(),
                status.HTTP_403_FORBIDDEN: forbidden_response(UserNotActiveError),
                status.HTTP_404_NOT_FOUND: not_found_response(UserNotFoundError),
            },
            summary='Update User PATCH',
        ),
        delete=extend_schema(
            parameters=[jwt_header_parameter()],
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
    return decorator(view)


def extend_set_password_user_view_schema(view):
    decorator = extend_schema_view(
        post=extend_schema(
            parameters=[jwt_header_parameter()],
            request=SetPasswordUserInSerializer,
            responses={
                status.HTTP_204_NO_CONTENT: None,
                status.HTTP_401_UNAUTHORIZED: unauthorized_user_response(),
                status.HTTP_403_FORBIDDEN: forbidden_response(UserNotActiveError),
                status.HTTP_404_NOT_FOUND: not_found_response(UserNotFoundError),
            },
            summary='Update User Password POST',
        )
    )
    return decorator(view)

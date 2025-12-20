from drf_spectacular.utils import OpenApiResponse, extend_schema, extend_schema_view
from rest_framework import status

from src.api.v1.common.serializers import DetailOutSerializer
from src.api.v1.users.serializers import PasswordUserSerializer, UpdateUserSerializer, UserSerializer
from src.apps.common.docs.schema_examples import (
    build_detail_response_example,
    build_response_example_from_error,
)
from src.apps.common.docs.schema_parameters import jwt_header_request_parameter
from src.apps.common.docs.schema_responses import unauthorized_error_401_response
from src.apps.users.exceptions.users import UserWithDataAlreadyExistsError


def _update_user_extend_schema(method: str):
    return extend_schema(
        parameters=[jwt_header_request_parameter()],
        request=UpdateUserSerializer,
        responses={
            status.HTTP_200_OK: OpenApiResponse(
                response=UpdateUserSerializer,
                description='User has been updated',
            ),
            status.HTTP_400_BAD_REQUEST: OpenApiResponse(
                response=DetailOutSerializer,
                description='User with the provided data already exists or the provided value is invalid',
                examples=[build_response_example_from_error(error=UserWithDataAlreadyExistsError)],
            ),
            status.HTTP_401_UNAUTHORIZED: unauthorized_error_401_response(),
        },
        summary=f'Update User {method}',
    )


def extend_user_view_schema():
    return extend_schema_view(
        post=extend_schema(
            request=UserSerializer,
            responses={
                status.HTTP_201_CREATED: OpenApiResponse(
                    response=UserSerializer,
                    description='User has been created',
                ),
                status.HTTP_400_BAD_REQUEST: OpenApiResponse(
                    response=DetailOutSerializer,
                    description='User with the provided data already exists or the provided value is invalid',
                    examples=[build_response_example_from_error(error=UserWithDataAlreadyExistsError)],
                ),
            },
            summary='Create User POST',
        ),
        get=extend_schema(
            parameters=[jwt_header_request_parameter()],
            request=None,
            responses={
                status.HTTP_200_OK: OpenApiResponse(
                    response=UserSerializer,
                    description='User has been retrieved',
                ),
                status.HTTP_401_UNAUTHORIZED: unauthorized_error_401_response(),
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
                status.HTTP_401_UNAUTHORIZED: unauthorized_error_401_response(),
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
                status.HTTP_200_OK: OpenApiResponse(
                    response=DetailOutSerializer,
                    description='Password has been updated',
                ),
                status.HTTP_401_UNAUTHORIZED: unauthorized_error_401_response(),
            },
            examples=[
                build_detail_response_example(name='Password updated', value='Success', status_code=200),
            ],
            summary='Update User Password POST',
        )
    )

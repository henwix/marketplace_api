from drf_spectacular.utils import OpenApiResponse, extend_schema, extend_schema_view
from rest_framework import status

from src.api.v1.common.serializers import DetailOutSerializer
from src.api.v1.users.serializers import PasswordUserSerializer, UpdateUserSerializer, UserSerializer
from src.apps.common.docs.response_examples import build_example_example_from_error, detail_response_example
from src.apps.users.exceptions.users import UserWithDataAlreadyExistsError

extend_user_viewset_schema = extend_schema_view(
    create=extend_schema(
        request=UserSerializer,
        responses={
            status.HTTP_201_CREATED: OpenApiResponse(
                response=UserSerializer,
                description='User has been created',
            ),
            status.HTTP_400_BAD_REQUEST: OpenApiResponse(
                response=DetailOutSerializer,
                description='User with the provided data already exists or the provided value is invalid',
            ),
        },
        examples=[
            build_example_example_from_error(error=UserWithDataAlreadyExistsError),
        ],
        summary='Create User',
    ),
    set_password=extend_schema(
        request=PasswordUserSerializer,
        responses={
            status.HTTP_200_OK: OpenApiResponse(
                response=DetailOutSerializer,
                description='Password has been updated',
            )
        },
        examples=[
            detail_response_example(name='Password updated', value='Success', status_code=200),
        ],
        summary='Update User Password',
    ),
    retrieve=extend_schema(
        responses=OpenApiResponse(response=UserSerializer, description='User has been retrieved'),
        summary='Retrieve User',
    ),
    update=extend_schema(
        responses=OpenApiResponse(response=UpdateUserSerializer, description='User has been updated'),
        summary='Update User PUT',
    ),
    partial_update=extend_schema(
        responses=OpenApiResponse(response=UpdateUserSerializer, description='User has been updated'),
        summary='Update User PATCH',
    ),
    destroy=extend_schema(summary='Delete User'),
)

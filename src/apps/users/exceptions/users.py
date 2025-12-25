from dataclasses import dataclass

from rest_framework import status

from src.apps.common.exceptions import ServiceException


@dataclass
class UserWithDataAlreadyExistsError(ServiceException):
    status_code = status.HTTP_400_BAD_REQUEST
    message = 'User with this data already exists'


@dataclass
class UserAuthNotFoundError(ServiceException):
    status_code = status.HTTP_401_UNAUTHORIZED
    message = 'User not found'
    user_id: int


@dataclass
class UserAuthNotActiveError(ServiceException):
    status_code = status.HTTP_401_UNAUTHORIZED
    message = 'User not active'
    user_id: int


@dataclass
class UserAuthCredentialsNotProvidedError(ServiceException):
    status_code = status.HTTP_401_UNAUTHORIZED
    message = 'Authentication credentials were not provided'

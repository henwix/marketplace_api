from dataclasses import dataclass

from rest_framework import status

from src.apps.common.exceptions import ServiceException


@dataclass
class UserWithDataAlreadyExistsError(ServiceException):
    status_code = status.HTTP_400_BAD_REQUEST
    message = 'User with this data already exists'


@dataclass
class UserNotFoundError(ServiceException):
    status_code = status.HTTP_404_NOT_FOUND
    message = 'User not found'
    user_id: int


@dataclass
class UserNotActiveError(ServiceException):
    status_code = status.HTTP_403_FORBIDDEN
    message = 'User not active'
    user_id: int

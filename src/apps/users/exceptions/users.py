from dataclasses import dataclass

from rest_framework import status

from src.apps.common.exceptions import ServiceException


@dataclass
class UserWithDataAlreadyExistsError(ServiceException):
    status_code = status.HTTP_400_BAD_REQUEST
    message = 'User with this data already exists'

from dataclasses import dataclass

from rest_framework import status

from src.apps.common.exceptions import ServiceException


@dataclass
class AuthCredentialsNotProvidedError(ServiceException):
    status_code = status.HTTP_401_UNAUTHORIZED
    message = 'Authentication credentials were not provided'

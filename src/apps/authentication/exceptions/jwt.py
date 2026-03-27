from dataclasses import dataclass

from rest_framework import status

from src.apps.common.exceptions.common import ServiceException


@dataclass(eq=False)
class JWTTokenInvalidError(ServiceException):
    status_code = status.HTTP_401_UNAUTHORIZED
    message = 'JWT token invalid'
    error_details: str

from dataclasses import dataclass

from rest_framework import status

from src.apps.common.exceptions.common import ServiceException


@dataclass(eq=False)
class AuthProviderAlreadyConnectedError(ServiceException):
    status_code = status.HTTP_400_BAD_REQUEST
    message = 'Auth provider already connected'
    current_user_id: int
    provider: str


@dataclass(eq=False)
class AuthProviderNotSupportedError(ServiceException):
    status_code = status.HTTP_400_BAD_REQUEST
    message = 'Auth provider is not supported'
    provider: str


@dataclass(eq=False)
class AuthProvidersNotFoundError(ServiceException):
    status_code = status.HTTP_404_NOT_FOUND
    message = 'No connected auth providers were found'


@dataclass(eq=False)
class AuthProviderNotConnectedError(ServiceException):
    status_code = status.HTTP_404_NOT_FOUND
    message = 'Auth provider not connected'
    user_id: int
    provider: str


@dataclass(eq=False)
class UnableToDisconnectAuthProviderError(ServiceException):
    status_code = status.HTTP_400_BAD_REQUEST
    message = 'Auth provider cannot be disconnected because at least one working login method must be present'
    provider: str

from dataclasses import dataclass

from rest_framework import status

from src.apps.common.exceptions.common import ServiceException


@dataclass(eq=False)
class OAuthIncorrectStateError(ServiceException):
    status_code = status.HTTP_400_BAD_REQUEST
    message = 'Incorrect state value'
    provider: str
    state: str


@dataclass(eq=False)
class OAuthIncorrectCodeError(ServiceException):
    status_code = status.HTTP_400_BAD_REQUEST
    message = 'Code is incorrect or expired'
    provider: str
    code: str


@dataclass(eq=False)
class OAuthInvalidTokenError(ServiceException):
    status_code = status.HTTP_401_UNAUTHORIZED
    message = 'Invalid OAuth authorization token'
    provider: str
    error_description: str


@dataclass(eq=False)
class OAuthNotSupportedProviderError(ServiceException):
    status_code = status.HTTP_400_BAD_REQUEST
    message = 'OAuth provider is not supported'
    provider: str


@dataclass(eq=False)
class OAuthUnverifiedProviderEmailError(ServiceException):
    status_code = status.HTTP_400_BAD_REQUEST
    message = 'OAuth provider account email is not verified'
    provider: str


@dataclass(eq=False)
class OAuthProviderEmailNotFoundError(ServiceException):
    status_code = status.HTTP_401_UNAUTHORIZED
    message = 'OAuth provider account email not found'
    provider: str


@dataclass(eq=False)
class OAuthProviderUidNotFoundError(ServiceException):
    status_code = status.HTTP_401_UNAUTHORIZED
    message = 'OAuth provider account uid not found'
    provider: str


@dataclass(eq=False)
class OAuthProviderRequestError(ServiceException):
    status_code = status.HTTP_502_BAD_GATEWAY
    message = 'Exception occured during OAuth provider request'
    provider: str
    error: str | None = None
    error_description: str | None = None

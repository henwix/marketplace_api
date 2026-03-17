from dataclasses import dataclass

from rest_framework import status

from src.apps.common.exceptions.common import ServiceException


@dataclass(eq=False)
class OAuthIncorrectStateError(ServiceException):
    status_code = status.HTTP_400_BAD_REQUEST
    message = 'Incorrect state value'
    state: str


@dataclass(eq=False)
class OAuthIncorrectCodeError(ServiceException):
    status_code = status.HTTP_400_BAD_REQUEST
    message = 'Code is incorrect or expired'
    code: str


@dataclass(eq=False)
class OAuthNotSupportedProviderError(ServiceException):
    status_code = status.HTTP_400_BAD_REQUEST
    message = 'OAuth provider is not supported'
    provider_name: str


@dataclass(eq=False)
class OAuthUnverifiedProviderEmailError(ServiceException):
    status_code = status.HTTP_400_BAD_REQUEST
    message = 'OAuth provider account email is not verified'


@dataclass(eq=False)
class OAuthProviderEmailNotFoundError(ServiceException):
    status_code = status.HTTP_400_BAD_REQUEST
    message = 'No email is linked to your OAuth provider account'


@dataclass(eq=False)
class OAuthProviderRequestError(ServiceException):
    status_code = status.HTTP_502_BAD_GATEWAY
    message = 'Exception occured during OAuth provider request'
    error: str | None
    code: str

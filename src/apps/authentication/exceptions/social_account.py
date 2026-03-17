from dataclasses import dataclass

from rest_framework import status

from src.apps.common.exceptions.common import ServiceException


@dataclass(eq=False)
class SocialAccountProviderAlreadyConnectedError(ServiceException):
    status_code = status.HTTP_400_BAD_REQUEST
    message = 'Provider already connected'
    current_user_id: int
    provider: str

from dataclasses import dataclass

from rest_framework import status

from src.apps.common.exceptions.common import ServiceException


@dataclass(eq=False)
class NothingToUpdateError(ServiceException):
    status_code = status.HTTP_400_BAD_REQUEST
    message = 'No fields provided to update'

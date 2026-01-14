from dataclasses import dataclass

from rest_framework import status


@dataclass(eq=False)
class ServiceException(Exception):
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    message = 'Application exception occured'

    @classmethod
    def response(cls) -> dict:
        return {'detail': cls.message}


@dataclass(eq=False)
class NothingToUpdateError(ServiceException):
    status_code = status.HTTP_400_BAD_REQUEST
    message = 'No fields provided to update'

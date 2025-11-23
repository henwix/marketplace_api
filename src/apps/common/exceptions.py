from dataclasses import dataclass

from rest_framework import status


@dataclass
class ServiceException(Exception):
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    message = 'Application exception occured'

    @property
    def response(self) -> dict:
        return {'detail': self.message}

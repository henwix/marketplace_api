from dataclasses import dataclass

from rest_framework import status

from src.apps.common.exceptions.common import ServiceException


@dataclass(eq=False)
class HTTPClientError(ServiceException):
    status_code = status.HTTP_502_BAD_GATEWAY
    message = 'Exception occured during request'
    method: str
    url: str
    response_status: int | None
    error_details: str

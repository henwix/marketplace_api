from dataclasses import dataclass
from uuid import UUID

from rest_framework import status

from src.apps.common.exceptions import ServiceException


@dataclass
class ProductNotFoundError(ServiceException):
    status_code = status.HTTP_404_NOT_FOUND
    message = 'Product not found'


@dataclass
class ProductAuthorPermissionError(ServiceException):
    status_code = status.HTTP_403_FORBIDDEN
    message = 'Product access forbidden'

    seller_id: int | None
    product_id: UUID

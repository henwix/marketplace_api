from dataclasses import dataclass
from uuid import UUID

from rest_framework import status

from src.apps.common.exceptions import ServiceException


@dataclass
class ProductNotFoundByIdError(ServiceException):
    status_code = status.HTTP_404_NOT_FOUND
    message = 'Product not found by id'
    id: UUID


@dataclass
class ProductNotFoundBySlugError(ServiceException):
    status_code = status.HTTP_404_NOT_FOUND
    message = 'Product not found by slug'
    slug: str


@dataclass
class ProductAccessForbiddenError(ServiceException):
    status_code = status.HTTP_403_FORBIDDEN
    message = 'Product access forbidden'
    product_id: UUID
    seller_id: int | None = None

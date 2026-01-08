from dataclasses import dataclass
from uuid import UUID

from rest_framework import status

from src.apps.common.exceptions import ServiceException


@dataclass(eq=False)
class ProductVariantNotFoundError(ServiceException):
    status_code = status.HTTP_404_NOT_FOUND
    message = 'Product variant not found'
    id: UUID


@dataclass(eq=False)
class ProductVariantsNotFoundError(ServiceException):
    status_code = status.HTTP_404_NOT_FOUND
    message = 'Product variants not found'
    product_id: UUID


@dataclass(eq=False)
class ProductVariantAccessForbiddenError(ServiceException):
    status_code = status.HTTP_403_FORBIDDEN
    message = 'Product variant access forbidden'
    product_variant_id: UUID
    seller_id: int | None = None


@dataclass(eq=False)
class ProductVariantsLimitError(ServiceException):
    status_code = status.HTTP_400_BAD_REQUEST
    message = 'Product variants limit has been reached'
    product_id: UUID
    variants_count: int
    variants_limit: int

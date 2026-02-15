from dataclasses import dataclass
from uuid import UUID

from rest_framework import status

from src.apps.common.exceptions import ServiceException


@dataclass
class ItemAlreadyInCartError(ServiceException):
    status_code = status.HTTP_400_BAD_REQUEST
    message = 'Item already in cart'
    cart_id: int
    product_variant_id: UUID


@dataclass
class ItemProductVariantOrSellerNotFoundError(ServiceException):
    status_code = status.HTTP_404_NOT_FOUND
    message = 'Product variant or seller not found'
    cart_id: int
    product_variant_id: UUID
    seller_id: int

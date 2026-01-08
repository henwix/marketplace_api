from dataclasses import dataclass
from uuid import UUID

from rest_framework import status

from src.apps.common.exceptions import ServiceException


@dataclass(eq=False)
class ProductReviewAlreadyExistsError(ServiceException):
    status_code = status.HTTP_400_BAD_REQUEST
    message = 'Product review already exists'
    user_id: int
    product_id: UUID


@dataclass(eq=False)
class ProductReviewNotFoundError(ServiceException):
    status_code = status.HTTP_404_NOT_FOUND
    message = 'Product review not found'
    user_id: int
    product_id: UUID

from dataclasses import dataclass
from uuid import UUID

from rest_framework import status

from src.apps.common.exceptions import ServiceException


@dataclass
class ProductReviewAlreadyExistsError(ServiceException):
    status_code = status.HTTP_400_BAD_REQUEST
    message = 'Product review already exists'
    user_id: int
    product_id: UUID


@dataclass
class ProductReviewNotFoundError(ServiceException):
    status_code = status.HTTP_400_BAD_REQUEST
    message = 'Product review not found'
    product_review_id: int


@dataclass
class ProductReviewAccessForbiddenError(ServiceException):
    status_code = status.HTTP_403_FORBIDDEN
    message = 'Product review access forbidden'
    user_id: int
    product_review_id: int

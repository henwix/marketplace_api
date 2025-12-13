from dataclasses import dataclass

from rest_framework import status

from src.apps.common.exceptions import ServiceException


@dataclass
class ProductVariantsLimitError(ServiceException):
    status_code = status.HTTP_400_BAD_REQUEST
    message = 'Product variants limit has been reached'

    variants_count: int
    variants_limit: int

from dataclasses import dataclass

from rest_framework import status

from src.apps.common.exceptions import ServiceException


@dataclass
class SellerAlreadyExistsError(ServiceException):
    status_code = status.HTTP_400_BAD_REQUEST
    message = 'Seller profile already exists'
    user_id: int


@dataclass
class SellerNotFoundError(ServiceException):
    status_code = status.HTTP_404_NOT_FOUND
    message = 'Seller profile not found'
    user_id: int | None = None


@dataclass
class SellerNotFoundByIdError(ServiceException):
    status_code = status.HTTP_404_NOT_FOUND
    message = 'Seller profile not found by id'
    id: int

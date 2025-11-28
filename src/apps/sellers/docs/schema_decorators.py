from drf_spectacular.utils import OpenApiResponse, extend_schema, extend_schema_view
from rest_framework import status

from src.api.v1.sellers.serializers import SellerSerializer

extend_seller_viewset_schema = extend_schema_view(
    create=extend_schema(
        request=SellerSerializer,
        responses={
            status.HTTP_201_CREATED: OpenApiResponse(
                response=SellerSerializer,
                description='Seller profile has been created',
            )
        },
        summary='Create Seller Profile',
    ),
    retrieve=extend_schema(
        responses=OpenApiResponse(response=SellerSerializer, description='Seller profile has been retrieved'),
        summary='Retrieve Seller Profile',
    ),
    update=extend_schema(
        responses=OpenApiResponse(response=SellerSerializer, description='Seller profile has been updated'),
        summary='Update Seller Profile PUT',
    ),
    partial_update=extend_schema(
        responses=OpenApiResponse(response=SellerSerializer, description='Seller profile has been updated'),
        summary='Update Seller Profile PATCH',
    ),
    destroy=extend_schema(summary='Delete Seller Profile'),
)

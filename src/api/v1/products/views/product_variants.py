from logging import Logger

import orjson
from punq import Container
from rest_framework import status
from rest_framework.views import APIView, Response

from src.api.v1.products.serializers.product_variants import ProductVariantSerializer
from src.apps.common.exceptions import ServiceException
from src.apps.products.docs.product_variants.schema_decorators import (
    extend_detail_product_variant_view_schema,
    extend_product_variant_view_schema,
)
from src.apps.products.use_cases.product_variants.create import CreateProductVariantUseCase
from src.apps.products.use_cases.product_variants.delete import DeleteProductVariantUseCase
from src.apps.products.use_cases.product_variants.update import UpdateProductVariantUseCase
from src.apps.sellers.converters.sellers import seller_to_entity
from src.apps.sellers.permissions import HasSellerProfilePermission, ReadOnlyOrHasSellerProfilePermission
from src.project.containers import get_container


@extend_product_variant_view_schema()
class ProductVariantView(APIView):
    permission_classes = [ReadOnlyOrHasSellerProfilePermission]

    def post(self, request, id):
        serializer = ProductVariantSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        container: Container = get_container()
        logger: Logger = container.resolve(Logger)
        use_case: CreateProductVariantUseCase = container.resolve(CreateProductVariantUseCase)

        try:
            variant = use_case.execute(
                seller=seller_to_entity(request.user.seller_profile),
                data=serializer.validated_data,
                product_id=id,
            )
            return Response(
                data=ProductVariantSerializer(variant).data,
                status=status.HTTP_201_CREATED,
            )
        except ServiceException as error:
            logger.error(msg=error.response(), extra={'log_meta': orjson.dumps(error).decode()})
            return Response(data=error.response(), status=error.status_code)

    def get(self, request, id):
        return Response({'request': 'get'})


@extend_detail_product_variant_view_schema()
class DetailProductVariantView(APIView):
    permission_classes = [HasSellerProfilePermission]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.container: Container = get_container()
        self.logger: Logger = self.container.resolve(Logger)

    def delete(self, request, id):
        use_case: DeleteProductVariantUseCase = self.container.resolve(DeleteProductVariantUseCase)

        try:
            use_case.execute(
                seller=seller_to_entity(request.user.seller_profile),
                product_variant_id=id,
            )
            return Response(status=status.HTTP_204_NO_CONTENT)
        except ServiceException as error:
            self.logger.error(msg=error.response(), extra={'log_meta': orjson.dumps(error).decode()})
            return Response(data=error.response(), status=error.status_code)

    # FIXME: created_at and updated_at not updating
    def update(self, request, id, partial: bool):
        serializer = ProductVariantSerializer(data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        use_case: UpdateProductVariantUseCase = self.container.resolve(UpdateProductVariantUseCase)

        try:
            product_variant = use_case.execute(
                seller=seller_to_entity(request.user.seller_profile),
                product_variant_id=id,
                data=serializer.validated_data,
            )
            return Response(data=ProductVariantSerializer(product_variant).data, status=status.HTTP_200_OK)
        except ServiceException as error:
            self.logger.error(msg=error.response(), extra={'log_meta': orjson.dumps(error).decode()})
            return Response(data=error.response(), status=error.status_code)

    def put(self, request, id):
        return self.update(request=request, id=id, partial=False)

    def patch(self, request, id):
        return self.update(request=request, id=id, partial=True)

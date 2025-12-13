from logging import Logger

import orjson
import punq
from rest_framework import status
from rest_framework.views import APIView, Response

from src.api.v1.products.serializers.product_variants import ProductVariantSerializer
from src.apps.common.exceptions import ServiceException
from src.apps.products.converters.product_variants import product_variant_from_entity
from src.apps.products.docs.product_variants.schema_decorators import extend_create_product_variant_schema
from src.apps.products.use_cases.product_variants.create import CreateProductVariantUseCase
from src.apps.sellers.converters.sellers import seller_to_entity
from src.apps.sellers.permissions import ReadOnlyOrHasSellerProfilePermission
from src.project.containers import get_container


@extend_create_product_variant_schema
class CreateProductVariantView(APIView):
    permission_classes = [ReadOnlyOrHasSellerProfilePermission]

    def post(self, request, id):
        serializer = ProductVariantSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        container: punq.Container = get_container()
        logger: Logger = container.resolve(Logger)
        use_case: CreateProductVariantUseCase = container.resolve(CreateProductVariantUseCase)

        try:
            variant = use_case.execute(
                seller=seller_to_entity(request.user.seller_profile),
                data=serializer.validated_data,
                product_id=id,
            )
            return Response(
                data=ProductVariantSerializer(product_variant_from_entity(entity=variant)).data,
                status=status.HTTP_201_CREATED,
            )
        except ServiceException as error:
            logger.error(msg=error.response(), extra={'log_meta': orjson.dumps(error).decode()})
            return Response(data=error.response(), status=error.status_code)

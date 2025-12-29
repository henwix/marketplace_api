from urllib.request import Request
from uuid import UUID

from punq import Container
from rest_framework import status
from rest_framework.views import APIView, Response

from src.api.v1.products.serializers.product_variants import ProductVariantSerializer
from src.apps.products.docs.product_variants.schema_decorators import (
    extend_detail_product_variant_view_schema,
    extend_product_variant_view_schema,
)
from src.apps.products.use_cases.product_variants.create import CreateProductVariantUseCase
from src.apps.products.use_cases.product_variants.delete import DeleteProductVariantUseCase
from src.apps.products.use_cases.product_variants.get import GetProductVariantsUseCase
from src.apps.products.use_cases.product_variants.update import UpdateProductVariantUseCase
from src.project.containers import get_container


@extend_product_variant_view_schema()
class ProductVariantView(APIView):
    def post(self, request: Request, id: UUID) -> Response:
        serializer = ProductVariantSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        container: Container = get_container()
        use_case: CreateProductVariantUseCase = container.resolve(CreateProductVariantUseCase)
        variant = use_case.execute(user_id=request.user.id, data=serializer.validated_data, product_id=id)
        return Response(data=ProductVariantSerializer(variant).data, status=status.HTTP_201_CREATED)

    def get(self, request: Request, id: UUID) -> Response:
        container: Container = get_container()
        use_case: GetProductVariantsUseCase = container.resolve(GetProductVariantsUseCase)
        variants_count, variants = use_case.execute(user_id=request.user.id, product_id=id)
        return Response(
            data={
                'count': variants_count,
                'results': ProductVariantSerializer(variants, many=True).data,
            },
            status=status.HTTP_200_OK,
        )


@extend_detail_product_variant_view_schema()
class DetailProductVariantView(APIView):
    def delete(self, request: Request, id: UUID) -> Response:
        container: Container = get_container()
        use_case: DeleteProductVariantUseCase = container.resolve(DeleteProductVariantUseCase)
        use_case.execute(user_id=request.user.id, product_variant_id=id)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def update(self, request: Request, id: UUID, partial: bool) -> Response:
        serializer = ProductVariantSerializer(data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        container: Container = get_container()
        use_case: UpdateProductVariantUseCase = container.resolve(UpdateProductVariantUseCase)
        product_variant = use_case.execute(
            user_id=request.user.id,
            product_variant_id=id,
            data=serializer.validated_data,
        )
        return Response(data=ProductVariantSerializer(product_variant).data, status=status.HTTP_200_OK)

    def put(self, request: Request, id: UUID) -> Response:
        return self.update(request=request, id=id, partial=False)

    def patch(self, request: Request, id: UUID) -> Response:
        return self.update(request=request, id=id, partial=True)

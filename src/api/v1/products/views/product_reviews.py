from uuid import UUID

from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from src.api.v1.products.openapi.product_reviews.decorators import (
    extend_detail_product_review_view_schema,
    extend_product_review_view_schema,
)
from src.api.v1.products.serializers.product_reviews import ProductReviewSerializer
from src.apps.products.commands.product_reviews import (
    CreateProductReviewCommand,
    DeleteProductReviewCommand,
    UpdateProductReviewCommand,
)
from src.apps.products.use_cases.product_reviews.create import CreateProductReviewUseCase
from src.apps.products.use_cases.product_reviews.delete import DeleteProductReviewUseCase
from src.apps.products.use_cases.product_reviews.update import UpdateProductReviewUseCase
from src.project.containers import resolve_depends


@extend_product_review_view_schema()
class ProductReviewView(APIView):
    def post(self, request: Request, id: UUID) -> Response:
        serializer = ProductReviewSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        use_case: CreateProductReviewUseCase = resolve_depends(CreateProductReviewUseCase)
        command = CreateProductReviewCommand(user_id=request.user.id, product_id=id, data=serializer.validated_data)
        review = use_case.execute(command=command)
        return Response(data=ProductReviewSerializer(review).data, status=status.HTTP_201_CREATED)

    def get(self, request: Request, id: UUID) -> Response:
        return Response(data={'id': id}, status=status.HTTP_200_OK)


@extend_detail_product_review_view_schema()
class DetailProductReviewView(APIView):
    def delete(self, request: Request, id: int) -> Response:
        use_case: DeleteProductReviewUseCase = resolve_depends(DeleteProductReviewUseCase)
        command = DeleteProductReviewCommand(user_id=request.user.id, product_review_id=id)
        use_case.execute(command=command)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def _update(self, request: Request, id: int, partial: bool) -> Response:
        serializer = ProductReviewSerializer(data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        use_case: UpdateProductReviewUseCase = resolve_depends(UpdateProductReviewUseCase)
        command = UpdateProductReviewCommand(
            user_id=request.user.id,
            product_review_id=id,
            data=serializer.validated_data,
        )
        review = use_case.execute(command=command)
        return Response(data=ProductReviewSerializer(review).data, status=status.HTTP_200_OK)

    def put(self, request: Request, id: int) -> Response:
        return self._update(request=request, id=id, partial=False)

    def patch(self, request: Request, id: int) -> Response:
        return self._update(request=request, id=id, partial=True)

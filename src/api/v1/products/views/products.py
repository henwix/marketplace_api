from uuid import UUID

import django_filters
from rest_framework import filters, status
from rest_framework.generics import GenericAPIView
from rest_framework.request import Request
from rest_framework.views import APIView, Response

from src.api.v1.common.mixins import LazyAuthViewMixin, PaginationViewMixin
from src.api.v1.products.filters import GlobalProductFilter, PersonalProductFilter
from src.api.v1.products.openapi.products.decorators import (
    extend_detail_product_view_schema,
    extend_detail_slug_product_view_schema,
    extend_global_search_view_schema,
    extend_personal_search_view_schema,
    extend_product_view_schema,
)
from src.api.v1.products.pagination import SearchProductPagination
from src.api.v1.products.serializers.products import (
    ProductSerializer,
    RetrieveProductSerializer,
    SearchProductSerializer,
)
from src.apps.products.use_cases.products.create import CreateProductUseCase
from src.apps.products.use_cases.products.delete import DeleteProductUseCase
from src.apps.products.use_cases.products.get_by_id import GetProductByIdUseCase
from src.apps.products.use_cases.products.get_by_slug import GetProductBySlugUseCase
from src.apps.products.use_cases.products.global_search import GlobalSearchProductUseCase
from src.apps.products.use_cases.products.personal_search import PersonalSearchProductUseCase
from src.apps.products.use_cases.products.update import UpdateProductUseCase
from src.project.containers import resolve_depends


@extend_product_view_schema()
class ProductView(APIView):
    def post(self, request: Request) -> Response:
        serializer = ProductSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        use_case: CreateProductUseCase = resolve_depends(CreateProductUseCase)
        product = use_case.execute(user_id=request.user.id, data=serializer.validated_data)
        return Response(data=ProductSerializer(product).data, status=status.HTTP_201_CREATED)


@extend_detail_slug_product_view_schema()
class DetailSlugProductView(APIView):
    def get(self, request: Request, slug: str) -> Response:
        use_case: GetProductBySlugUseCase = resolve_depends(GetProductBySlugUseCase)
        product = use_case.execute(user_id=request.user.id, slug=slug)
        return Response(
            data=RetrieveProductSerializer(product, context={'request': self.request}).data,
            status=status.HTTP_200_OK,
        )


@extend_detail_product_view_schema()
class DetailProductView(APIView):
    def get(self, request: Request, id: UUID) -> Response:
        use_case: GetProductByIdUseCase = resolve_depends(GetProductByIdUseCase)
        product = use_case.execute(user_id=request.user.id, product_id=id)
        return Response(
            data=RetrieveProductSerializer(product, context={'request': self.request}).data,
            status=status.HTTP_200_OK,
        )

    def delete(self, request: Request, id: UUID) -> Response:
        use_case: DeleteProductUseCase = resolve_depends(DeleteProductUseCase)
        use_case.execute(user_id=request.user.id, product_id=id)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def update(self, request: Request, id: UUID, partial: bool) -> Response:
        serializer = ProductSerializer(data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        use_case: UpdateProductUseCase = resolve_depends(UpdateProductUseCase)
        product = use_case.execute(user_id=request.user.id, product_id=id, data=serializer.validated_data)
        return Response(data=ProductSerializer(product).data, status=status.HTTP_200_OK)

    def put(self, request: Request, id: UUID) -> Response:
        return self.update(request=request, id=id, partial=False)

    def patch(self, request: Request, id: UUID) -> Response:
        return self.update(request=request, id=id, partial=True)


# TODO: cache for searching
@extend_global_search_view_schema()
class GlobalSearchProductView(
    PaginationViewMixin,
    LazyAuthViewMixin,
    GenericAPIView,
):
    filterset_class = GlobalProductFilter
    filter_backends = [
        filters.SearchFilter,
        filters.OrderingFilter,
        django_filters.rest_framework.DjangoFilterBackend,
    ]
    search_fields = ['title', 'description', 'short_description']
    ordering_fields = ['created_at', 'updated_at', 'price']
    ordering = ['-created_at']

    def get(self, request: Request) -> Response:
        use_case: GlobalSearchProductUseCase = resolve_depends(GlobalSearchProductUseCase)
        products = use_case.execute()
        return self.paginate(
            queryset=products,
            paginator=SearchProductPagination,
            serializer=SearchProductSerializer,
        )


@extend_personal_search_view_schema()
class PersonalSearchProductView(
    PaginationViewMixin,
    GenericAPIView,
):
    filterset_class = PersonalProductFilter
    filter_backends = [
        filters.SearchFilter,
        filters.OrderingFilter,
        django_filters.rest_framework.DjangoFilterBackend,
    ]
    search_fields = ['title', 'description', 'short_description']
    ordering_fields = ['created_at', 'updated_at', 'price']
    ordering = ['-created_at']

    def get(self, request: Request) -> Response:
        use_case: PersonalSearchProductUseCase = resolve_depends(PersonalSearchProductUseCase)
        products = use_case.execute(user_id=request.user.id)
        return self.paginate(
            queryset=products,
            paginator=SearchProductPagination,
            serializer=SearchProductSerializer,
        )

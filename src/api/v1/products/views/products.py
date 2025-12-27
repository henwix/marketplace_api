from uuid import UUID

import django_filters
from punq import Container
from rest_framework import filters, status
from rest_framework.generics import ListAPIView
from rest_framework.request import Request
from rest_framework.views import APIView, Response

from src.api.v1.products.serializers.products import (
    ProductSerializer,
    RetrieveProductSerializer,
    SearchProductSerializer,
)
from src.apps.products.docs.products.schema_decorators import (
    extend_detail_product_view_schema,
    extend_detail_slug_product_view_schema,
    extend_global_search_view_schema,
    extend_personal_search_view_schema,
    extend_product_view_schema,
)
from src.apps.products.filters import GlobalProductFilter, PersonalProductFilter
from src.apps.products.pagination import ProductPagination
from src.apps.products.repositories.products import BaseProductRepository
from src.apps.products.use_cases.products.create import CreateProductUseCase
from src.apps.products.use_cases.products.delete import DeleteProductUseCase
from src.apps.products.use_cases.products.get_by_id import GetProductByIdUseCase
from src.apps.products.use_cases.products.get_by_slug import GetProductBySlugUseCase
from src.apps.products.use_cases.products.update import UpdateProductUseCase
from src.apps.sellers.permissions import HasSellerProfilePermission
from src.project.containers import get_container


@extend_product_view_schema()
class ProductView(APIView):
    def post(self, request: Request) -> Response:
        serializer = ProductSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        container: Container = get_container()
        use_case: CreateProductUseCase = container.resolve(CreateProductUseCase)
        product = use_case.execute(user_id=request.user.id, data=serializer.validated_data)
        return Response(data=ProductSerializer(product).data, status=status.HTTP_201_CREATED)


@extend_detail_slug_product_view_schema()
class DetailSlugProductView(APIView):
    def get(self, request: Request, slug: str) -> Response:
        container: Container = get_container()
        use_case: GetProductBySlugUseCase = container.resolve(GetProductBySlugUseCase)
        product = use_case.execute(user_id=request.user.id, slug=slug)
        return Response(
            data=RetrieveProductSerializer(product, context={'request': self.request}).data,
            status=status.HTTP_200_OK,
        )


@extend_detail_product_view_schema()
class DetailProductView(APIView):
    def get(self, request: Request, id: UUID) -> Response:
        container: Container = get_container()
        use_case: GetProductByIdUseCase = container.resolve(GetProductByIdUseCase)
        product = use_case.execute(user_id=request.user.id, product_id=id)
        return Response(
            data=RetrieveProductSerializer(product, context={'request': self.request}).data,
            status=status.HTTP_200_OK,
        )

    def delete(self, request: Request, id: UUID) -> Response:
        container: Container = get_container()
        use_case: DeleteProductUseCase = container.resolve(DeleteProductUseCase)
        use_case.execute(user_id=request.user.id, product_id=id)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def update(self, request: Request, id: UUID, partial: bool) -> Response:
        serializer = ProductSerializer(data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        container: Container = get_container()
        use_case: UpdateProductUseCase = container.resolve(UpdateProductUseCase)
        product = use_case.execute(user_id=request.user.id, product_id=id, data=serializer.validated_data)
        return Response(data=ProductSerializer(product).data, status=status.HTTP_200_OK)

    def put(self, request: Request, id: UUID) -> Response:
        return self.update(request=request, id=id, partial=False)

    def patch(self, request: Request, id: UUID) -> Response:
        return self.update(request=request, id=id, partial=True)


# TODO: cache for searching
@extend_global_search_view_schema()
class GlobalSearchProductView(ListAPIView):
    serializer_class = SearchProductSerializer
    pagination_class = ProductPagination
    filterset_class = GlobalProductFilter
    filter_backends = [
        filters.SearchFilter,
        filters.OrderingFilter,
        django_filters.rest_framework.DjangoFilterBackend,
    ]
    search_fields = ['title', 'description', 'short_description']
    ordering_fields = ['created_at', 'updated_at', 'price']
    ordering = ['-created_at']

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.container: Container = get_container()
        self.repository: BaseProductRepository = self.container.resolve(BaseProductRepository)

    def get_queryset(self):
        return self.repository.get_many_for_global_search()

    def perform_authentication(self, request): ...


@extend_personal_search_view_schema()
class PersonalSearchProductView(GlobalSearchProductView):
    filterset_class = PersonalProductFilter
    permission_classes = [HasSellerProfilePermission]

    def get_queryset(self):
        return self.repository.get_many_for_personal_search(seller_id=self.request.user.seller_profile.id)

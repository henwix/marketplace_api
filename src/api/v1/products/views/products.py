from logging import Logger

import django_filters
import orjson
from punq import Container
from rest_framework import filters, status
from rest_framework.generics import ListAPIView
from rest_framework.views import APIView, Response

from src.api.v1.products.serializers.products import (
    ProductSerializer,
    RetrieveProductSerializer,
    SearchProductSerializer,
)
from src.apps.common.exceptions import ServiceException
from src.apps.products.docs.products.schema_decorators import (
    extend_create_product_view_schema,
    extend_detail_product_view_schema,
    extend_get_product_by_slug_view_schema,
    extend_global_search_view_schema,
    extend_personal_search_view_schema,
)
from src.apps.products.filters import GlobalProductFilter, PersonalProductFilter
from src.apps.products.models.products import Product
from src.apps.products.pagination import ProductPagination
from src.apps.products.repositories.products import BaseProductRepository
from src.apps.products.use_cases.products.create import CreateProductUseCase
from src.apps.products.use_cases.products.delete import DeleteProductUseCase
from src.apps.products.use_cases.products.get_by_id import GetProductByIdUseCase
from src.apps.products.use_cases.products.get_by_slug import GetProductBySlugUseCase
from src.apps.products.use_cases.products.update import UpdateProductUseCase
from src.apps.sellers.converters.sellers import seller_to_entity
from src.apps.sellers.permissions import HasSellerProfilePermission, ReadOnlyOrHasSellerProfilePermission
from src.project.containers import get_container


@extend_create_product_view_schema()
class CreateProductView(APIView):
    permission_classes = [ReadOnlyOrHasSellerProfilePermission]

    def post(self, request):
        serializer = ProductSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        container: Container = get_container()
        use_case: CreateProductUseCase = container.resolve(CreateProductUseCase)

        product = use_case.execute(
            seller_id=request.user.seller_profile.id,
            data=serializer.validated_data,
        )
        return Response(
            data=ProductSerializer(product).data,
            status=status.HTTP_201_CREATED,
        )


@extend_get_product_by_slug_view_schema()
class GetProductBySlugView(APIView):
    def get(self, request, slug):
        container: Container = get_container()
        logger: Logger = container.resolve(Logger)
        use_case: GetProductBySlugUseCase = container.resolve(GetProductBySlugUseCase)

        try:
            product = use_case.execute(
                seller=seller_to_entity(dto=getattr(request.user, 'seller_profile', None)),
                slug=slug,
            )
            return Response(
                data=RetrieveProductSerializer(product, context={'request': self.request}).data,
                status=status.HTTP_200_OK,
            )
        except ServiceException as error:
            logger.error(msg=error.message, extra={'log_meta': orjson.dumps(error).decode()})
            return Response(data=error.response(), status=error.status_code)


@extend_detail_product_view_schema()
class DetailProductView(APIView):
    permission_classes = [ReadOnlyOrHasSellerProfilePermission]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.container: Container = get_container()
        self.logger: Logger = self.container.resolve(Logger)

    # FIXME: fix an issue where product author cannot see invisible variants when retrieving product
    def get(self, request, id):
        use_case: GetProductByIdUseCase = self.container.resolve(GetProductByIdUseCase)

        try:
            product = use_case.execute(
                seller=seller_to_entity(dto=getattr(request.user, 'seller_profile', None)),
                product_id=id,
            )
            return Response(
                data=RetrieveProductSerializer(product, context={'request': self.request}).data,
                status=status.HTTP_200_OK,
            )
        except ServiceException as error:
            self.logger.error(msg=error.message, extra={'log_meta': orjson.dumps(error).decode()})
            return Response(data=error.response(), status=error.status_code)

    def delete(self, request, id):
        use_case: DeleteProductUseCase = self.container.resolve(DeleteProductUseCase)

        try:
            use_case.execute(
                seller=seller_to_entity(dto=request.user.seller_profile),
                product_id=id,
            )
            return Response(status=status.HTTP_204_NO_CONTENT)
        except ServiceException as error:
            self.logger.error(msg=error.message, extra={'log_meta': orjson.dumps(error).decode()})
            return Response(data=error.response(), status=error.status_code)

    def update(self, request, id, partial: bool):
        serializer = ProductSerializer(data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        use_case: UpdateProductUseCase = self.container.resolve(UpdateProductUseCase)

        try:
            product = use_case.execute(
                seller=seller_to_entity(dto=request.user.seller_profile),
                product_id=id,
                data=serializer.validated_data,
            )
            return Response(
                data=ProductSerializer(product).data,
                status=status.HTTP_200_OK,
            )
        except ServiceException as error:
            self.logger.error(msg=error.message, extra={'log_meta': orjson.dumps(error).decode()})
            return Response(data=error.response(), status=error.status_code)

    def put(self, request, id):
        return self.update(request=request, id=id, partial=False)

    def patch(self, request, id):
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
        if not self.request.user.is_authenticated:
            return Product.objects.all()
        return self.repository.get_many_for_personal_search(seller_id=self.request.user.seller_profile.id)

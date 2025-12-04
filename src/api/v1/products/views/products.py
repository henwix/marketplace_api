import django_filters
import punq
from rest_framework import filters, status
from rest_framework.views import Response
from rest_framework.viewsets import ModelViewSet

from src.api.v1.products.serializers.products import ProductSerializer
from src.apps.products.filters import ProductFilter
from src.apps.products.models.products import Product
from src.apps.products.pagination import ProductPagination
from src.apps.products.permissions import ProductPermission
from src.apps.products.use_cases.create_product import CreateProductUseCase
from src.project.containers import get_container


class ProductViewSet(ModelViewSet):
    serializer_class = ProductSerializer
    pagination_class = ProductPagination
    permission_classes = [ProductPermission]
    filter_backends = [
        filters.SearchFilter,
        filters.OrderingFilter,
        django_filters.rest_framework.DjangoFilterBackend,
    ]
    filterset_class = ProductFilter
    ordering_fields = ['created_at', 'updated_at']
    search_fields = ['title', 'description', 'short_description']
    ordering = ['-created_at']
    lookup_field = 'id'
    lookup_url_kwarg = 'id'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.container: punq.Container = get_container()

    def filter_queryset(self, queryset):
        if self.action == 'list':
            return super().filter_queryset(queryset)

    def get_queryset(self):
        if not self.request.user.is_authenticated:
            return Product.objects.all()
        return Product.objects.filter(seller_id=self.request.user.seller_profile.id)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        use_case: CreateProductUseCase = self.container.resolve(CreateProductUseCase)

        result = use_case.execute(
            seller_id=request.user.seller_profile.id,
            data=serializer.validated_data,
        )
        return Response(data=self.get_serializer(result).data, status=status.HTTP_201_CREATED)

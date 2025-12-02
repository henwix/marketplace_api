import punq
from rest_framework import status
from rest_framework.views import Response
from rest_framework.viewsets import ModelViewSet

from src.api.v1.products.serializers.products import ProductSerializer
from src.apps.products.models.products import Product
from src.apps.products.permissions import ProductPermission
from src.apps.products.use_cases.create_product import CreateProductUseCase
from src.project.containers import get_container


# TODO: list and search for user products
class ProductViewSet(ModelViewSet):
    serializer_class = ProductSerializer
    permission_classes = [ProductPermission]
    lookup_field = 'uuid'
    lookup_url_kwarg = 'uuid'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.container: punq.Container = get_container()

    def get_queryset(self):
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

import punq
from rest_framework import status
from rest_framework.mixins import CreateModelMixin, DestroyModelMixin, RetrieveModelMixin, UpdateModelMixin
from rest_framework.views import Response
from rest_framework.viewsets import GenericViewSet

from src.api.v1.sellers.serializers import SellerSerializer
from src.apps.sellers.docs.schema_decorators import extend_seller_viewset_schema
from src.apps.sellers.models import Seller
from src.apps.sellers.permissions import SellerPermission
from src.apps.sellers.use_cases.create import CreateSellerUseCase
from src.project.containers import get_container


@extend_seller_viewset_schema
class SellerViewSet(
    CreateModelMixin,
    RetrieveModelMixin,
    UpdateModelMixin,
    DestroyModelMixin,
    GenericViewSet,
):
    queryset = Seller.objects.all()
    permission_classes = [SellerPermission]
    serializer_class = SellerSerializer

    def get_object(self):
        return self.request.user.seller_profile

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        container: punq.Container = get_container()
        use_case: CreateSellerUseCase = container.resolve(CreateSellerUseCase)

        result = use_case.execute(user_id=request.user.pk, data=serializer.validated_data)
        return Response(data=self.get_serializer(result).data, status=status.HTTP_201_CREATED)

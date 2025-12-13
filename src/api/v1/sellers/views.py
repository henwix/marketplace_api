import punq
from rest_framework import status
from rest_framework.mixins import CreateModelMixin, DestroyModelMixin, RetrieveModelMixin, UpdateModelMixin
from rest_framework.permissions import AllowAny
from rest_framework.views import Response
from rest_framework.viewsets import GenericViewSet

from src.api.v1.sellers.serializers import SellerSerializer
from src.apps.sellers.converters.sellers import seller_from_entity
from src.apps.sellers.docs.schema_decorators import extend_seller_viewset_schema
from src.apps.sellers.models import Seller
from src.apps.sellers.permissions import SellerViewPermission
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
    lookup_field = 'id'
    lookup_url_kwarg = 'id'
    serializer_class = SellerSerializer

    def get_object(self):
        if self.action == 'get_by_id':
            return super().get_object()
        return self.request.user.seller_profile

    def get_permissions(self):
        if self.action == 'get_by_id':
            return [AllowAny()]
        return [SellerViewPermission()]

    def perform_authentication(self, request): ...

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        container: punq.Container = get_container()
        use_case: CreateSellerUseCase = container.resolve(CreateSellerUseCase)

        seller = use_case.execute(user_id=request.user.pk, data=serializer.validated_data)
        return Response(
            data=self.get_serializer(seller_from_entity(seller)).data,
            status=status.HTTP_201_CREATED,
        )

    def get_by_id(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

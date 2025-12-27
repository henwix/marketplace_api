from punq import Container
from rest_framework import status
from rest_framework.request import Request
from rest_framework.views import APIView, Response

from src.api.v1.sellers.serializers import SellerSerializer
from src.apps.sellers.docs.schema_decorators import (
    extend_detail_seller_view_schema,
    extend_seller_view_schema,
)
from src.apps.sellers.use_cases.create import CreateSellerUseCase
from src.apps.sellers.use_cases.delete import DeleteSellerUseCase
from src.apps.sellers.use_cases.get import GetSellerUseCase
from src.apps.sellers.use_cases.get_by_id import GetSellerByIdUseCase
from src.apps.sellers.use_cases.update import UpdateSellerUseCase
from src.project.containers import get_container


@extend_seller_view_schema()
class SellerView(APIView):
    def post(self, request: Request) -> Response:
        serializer = SellerSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        container: Container = get_container()
        use_case: CreateSellerUseCase = container.resolve(CreateSellerUseCase)
        seller = use_case.execute(user_id=request.user.id, data=serializer.validated_data)
        return Response(data=SellerSerializer(seller).data, status=status.HTTP_201_CREATED)

    def get(self, request: Request) -> Response:
        container: Container = get_container()
        use_case: GetSellerUseCase = container.resolve(GetSellerUseCase)
        seller = use_case.execute(user_id=request.user.id)
        return Response(data=SellerSerializer(seller).data, status=status.HTTP_200_OK)

    def update(self, request: Request, partial: bool) -> Response:
        serializer = SellerSerializer(data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        container: Container = get_container()
        use_case: UpdateSellerUseCase = container.resolve(UpdateSellerUseCase)
        seller = use_case.execute(user_id=request.user.id, data=serializer.validated_data)
        return Response(data=SellerSerializer(seller).data, status=status.HTTP_200_OK)

    def put(self, request: Request) -> Response:
        return self.update(request=request, partial=False)

    def patch(self, request: Request) -> Response:
        return self.update(request=request, partial=True)

    def delete(self, request: Request) -> Response:
        container: Container = get_container()
        use_case: DeleteSellerUseCase = container.resolve(DeleteSellerUseCase)
        use_case.execute(user_id=request.user.id)
        return Response(status=status.HTTP_204_NO_CONTENT)


@extend_detail_seller_view_schema()
class DetailSellerView(APIView):
    def get(self, request: Request, id: int) -> Response:
        container: Container = get_container()
        use_case: GetSellerByIdUseCase = container.resolve(GetSellerByIdUseCase)
        seller = use_case.execute(seller_id=id)
        return Response(data=SellerSerializer(seller).data, status=status.HTTP_200_OK)

    def perform_authentication(self, request): ...

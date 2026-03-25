from rest_framework import status
from rest_framework.request import Request
from rest_framework.views import APIView, Response

from src.api.v1.common.mixins import LazyAuthViewMixin
from src.api.v1.sellers.openapi.decorators import (
    extend_detail_seller_view_schema,
    extend_seller_view_schema,
)
from src.api.v1.sellers.serializers import CreateSellerInSerializer, SellerOutSerializer, UpdateSellerInSerializer
from src.apps.sellers.commands import (
    CreateSellerCommand,
    DeleteSellerCommand,
    GetSellerByIdCommand,
    GetSellerCommand,
    UpdateSellerCommand,
)
from src.apps.sellers.use_cases.create import CreateSellerUseCase
from src.apps.sellers.use_cases.delete import DeleteSellerUseCase
from src.apps.sellers.use_cases.get import GetSellerUseCase
from src.apps.sellers.use_cases.get_by_id import GetSellerByIdUseCase
from src.apps.sellers.use_cases.update import UpdateSellerUseCase
from src.project.containers import resolve_depends


@extend_seller_view_schema
class SellerView(APIView):
    def post(self, request: Request) -> Response:
        request_data = CreateSellerInSerializer.validate_data(data=request.data)
        use_case: CreateSellerUseCase = resolve_depends(CreateSellerUseCase)
        command = CreateSellerCommand(user_id=request.user.id, **request_data)
        seller = use_case.execute(command=command)
        return Response(data=SellerOutSerializer(seller).data, status=status.HTTP_201_CREATED)

    def get(self, request: Request) -> Response:
        use_case: GetSellerUseCase = resolve_depends(GetSellerUseCase)
        command = GetSellerCommand(user_id=request.user.id)
        seller = use_case.execute(command=command)
        return Response(data=SellerOutSerializer(seller).data, status=status.HTTP_200_OK)

    def delete(self, request: Request) -> Response:
        use_case: DeleteSellerUseCase = resolve_depends(DeleteSellerUseCase)
        command = DeleteSellerCommand(user_id=request.user.id)
        use_case.execute(command=command)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def _update(self, request: Request, partial: bool) -> Response:
        request_data = UpdateSellerInSerializer.validate_data(data=request.data, partial=partial)
        use_case: UpdateSellerUseCase = resolve_depends(UpdateSellerUseCase)
        command = UpdateSellerCommand(user_id=request.user.id, **request_data)
        seller = use_case.execute(command=command)
        return Response(data=SellerOutSerializer(seller).data, status=status.HTTP_200_OK)

    def put(self, request: Request) -> Response:
        return self._update(request=request, partial=False)

    def patch(self, request: Request) -> Response:
        return self._update(request=request, partial=True)


@extend_detail_seller_view_schema
class DetailSellerView(LazyAuthViewMixin, APIView):
    def get(self, request: Request, id: int) -> Response:
        use_case: GetSellerByIdUseCase = resolve_depends(GetSellerByIdUseCase)
        command = GetSellerByIdCommand(seller_id=id)
        seller = use_case.execute(command=command)
        return Response(data=SellerOutSerializer(seller).data, status=status.HTTP_200_OK)

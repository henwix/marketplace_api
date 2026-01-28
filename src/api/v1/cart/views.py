from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from src.api.v1.cart.openapi.decorators import extend_cart_view_schema
from src.api.v1.cart.serializers import AddItemToCartInSerializer
from src.apps.cart.commands import AddItemToCartCommand
from src.apps.cart.use_cases.add_item_to_cart import AddItemToCartUseCase
from src.project.containers import resolve_depends


@extend_cart_view_schema
class CartView(APIView):
    def post(self, request: Request) -> Response:
        serializer = AddItemToCartInSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        use_case: AddItemToCartUseCase = resolve_depends(AddItemToCartUseCase)
        command = AddItemToCartCommand(user_id=request.user.id, **serializer.validated_data)
        use_case.execute(command=command)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def get(self, request: Request) -> Response:
        return Response({'get': True})

    def delete(self, request: Request) -> Response:
        return Response({'delete': True})

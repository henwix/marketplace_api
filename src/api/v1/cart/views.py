from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from src.api.v1.cart.openapi.decorators import extend_cart_view_schema, extend_clear_cart_view_schema
from src.api.v1.cart.serializers import AddCartItemInSerializer, CartItemOutSerializer, DeleteCartItemInSerializer
from src.apps.cart.commands import AddCartItemCommand, ClearCartCommand, DeleteCartItemCommand, GetCartCommand
from src.apps.cart.use_cases.add_cart_item import AddCartItemUseCase
from src.apps.cart.use_cases.clear_cart import ClearCartUseCase
from src.apps.cart.use_cases.delete_cart_item import DeleteCartItemUseCase
from src.apps.cart.use_cases.get_cart import GetCartUseCase
from src.project.containers import resolve_depends


@extend_cart_view_schema
class CartView(APIView):
    def post(self, request: Request) -> Response:
        request_data = AddCartItemInSerializer.validate_data(data=request.data)
        use_case: AddCartItemUseCase = resolve_depends(AddCartItemUseCase)
        command = AddCartItemCommand(user_id=request.user.id, **request_data)
        cart_item = use_case.execute(command=command)
        return Response(CartItemOutSerializer(cart_item).data, status=status.HTTP_201_CREATED)

    def get(self, request: Request) -> Response:
        use_case: GetCartUseCase = resolve_depends(GetCartUseCase)
        command = GetCartCommand(user_id=request.user.id)
        cart_items, total_cart_price, cart_items_count = use_case.execute(command=command)
        return Response(
            data={
                'total_cart_price': total_cart_price,
                'cart_items_count': cart_items_count,
                'results': CartItemOutSerializer(cart_items, many=True).data,
            },
            status=status.HTTP_200_OK,
        )

    def delete(self, request: Request) -> Response:
        request_data = DeleteCartItemInSerializer.validate_data(data=request.query_params)
        use_case: DeleteCartItemUseCase = resolve_depends(DeleteCartItemUseCase)
        command = DeleteCartItemCommand(user_id=request.user.id, **request_data)
        use_case.execute(command=command)
        return Response(status=status.HTTP_204_NO_CONTENT)


@extend_clear_cart_view_schema
class ClearCartView(APIView):
    def delete(self, request: Request) -> Response:
        use_case: ClearCartUseCase = resolve_depends(ClearCartUseCase)
        command = ClearCartCommand(user_id=request.user.id)
        use_case.execute(command=command)
        return Response(status=status.HTTP_204_NO_CONTENT)

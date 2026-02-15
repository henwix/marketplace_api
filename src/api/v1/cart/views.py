from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from src.api.v1.cart.openapi.decorators import extend_cart_view_schema
from src.api.v1.cart.serializers import AddItemToCartInSerializer, CartItemOutSerializer
from src.apps.cart.commands import AddItemToCartCommand
from src.apps.cart.models import Cart, CartItem
from src.apps.cart.use_cases.add_item_to_cart import AddItemToCartUseCase
from src.project.containers import resolve_depends


@extend_cart_view_schema
class CartView(APIView):
    def post(self, request: Request) -> Response:
        serializer = AddItemToCartInSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        use_case: AddItemToCartUseCase = resolve_depends(AddItemToCartUseCase)
        command = AddItemToCartCommand(user_id=request.user.id, **serializer.validated_data)
        cart_item = use_case.execute(command=command)
        return Response(CartItemOutSerializer(cart_item).data, status=status.HTTP_201_CREATED)

    def get(self, request: Request) -> Response:
        cart = Cart.objects.filter(user_id=request.user.id).first()
        if cart is not None:
            items = CartItem.objects.filter(cart=cart).order_by('-created_at')
            return Response(CartItemOutSerializer(items, many=True).data)
        return Response({'detail': 'Cart not found'})

    def delete(self, request: Request) -> Response:
        return Response({'delete': True})

from django.urls import path

from src.api.v1.cart.views import CartView, ClearCartView

urlpatterns = [
    path('cart/', CartView.as_view(), name='cart'),
    path('cart/clear/', ClearCartView.as_view(), name='cart-clear'),
]

from django.urls import path

from src.api.v1.cart.views import CartView

urlpatterns = [
    path('cart/', CartView.as_view(), name='cart'),
]

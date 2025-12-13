from django.urls import include, path

from src.api.v1.sellers.views import SellerViewSet
from src.apps.sellers.routers import CustomSellersRouter

app_name = 'sellers'

seller_router = CustomSellersRouter()
seller_router.register(prefix='sellers', viewset=SellerViewSet, basename='sellers')


urlpatterns = [
    path('', include(seller_router.urls)),
]

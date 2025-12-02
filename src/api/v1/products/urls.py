from django.urls import include, path
from rest_framework.routers import SimpleRouter

from src.api.v1.products.views.products import ProductViewSet

app_name = 'products'

router = SimpleRouter()
router.register(prefix='products', viewset=ProductViewSet, basename='products')

urlpatterns = [
    path('', include(router.urls)),
]

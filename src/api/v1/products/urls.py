from django.urls import path

from src.api.v1.products.views.product_variants import CreateProductVariantView
from src.api.v1.products.views.products import (
    CreateProductApiView,
    DetailProductView,
    GetProductBySlugView,
    GlobalSearchProductView,
)

app_name = 'products'

urlpatterns = [
    path('products/', CreateProductApiView.as_view(), name='products-create'),
    path('products/search/', GlobalSearchProductView.as_view(), name='products-search'),
    path('products/<uuid:id>/', DetailProductView.as_view(), name='products-detail'),
    path('products/slug/<slug:slug>/', GetProductBySlugView.as_view(), name='products-get-by-slug'),
    path('products/<uuid:id>/variants/', CreateProductVariantView.as_view(), name='products-variant-create'),
]

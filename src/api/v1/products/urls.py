from django.urls import path

from src.api.v1.products.views.product_variants import DetailProductVariantView, ProductVariantView
from src.api.v1.products.views.products import (
    CreateProductView,
    DetailProductView,
    GetProductBySlugView,
    GlobalSearchProductView,
    PersonalSearchProductView,
)

app_name = 'products'

urlpatterns = [
    path('products/', CreateProductView.as_view(), name='products'),
    path('products/search/', GlobalSearchProductView.as_view(), name='products-search'),
    path('products/personal/', PersonalSearchProductView.as_view(), name='products-personal'),
    path('products/<uuid:id>/', DetailProductView.as_view(), name='products-detail'),
    path('products/slug/<slug:slug>/', GetProductBySlugView.as_view(), name='products-slug'),
    path('products/<uuid:id>/variants/', ProductVariantView.as_view(), name='product-variants'),
    path('product-variants/<uuid:id>/', DetailProductVariantView.as_view(), name='product-variants-detail'),
]

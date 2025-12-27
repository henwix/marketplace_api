from django.urls import path

from src.api.v1.products.views.product_variants import DetailProductVariantView, ProductVariantView
from src.api.v1.products.views.products import (
    DetailProductView,
    DetailSlugProductView,
    GlobalSearchProductView,
    PersonalSearchProductView,
    ProductView,
)

app_name = 'products'

urlpatterns = [
    path('products/', ProductView.as_view(), name='products'),
    path('products/search/', GlobalSearchProductView.as_view(), name='products-global-search'),
    path('products/personal/', PersonalSearchProductView.as_view(), name='products-personal-search'),
    path('products/<uuid:id>/', DetailProductView.as_view(), name='products-detail'),
    path('products/slug/<slug:slug>/', DetailSlugProductView.as_view(), name='products-slug-detail'),
    path('products/<uuid:id>/variants/', ProductVariantView.as_view(), name='product-variants'),
    path('product-variants/<uuid:id>/', DetailProductVariantView.as_view(), name='product-variants-detail'),
]

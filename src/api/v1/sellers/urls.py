from django.urls import path

from src.api.v1.sellers.views import DetailSellerView, SellerView

app_name = 'sellers'


urlpatterns = [
    path('sellers/', SellerView.as_view(), name='sellers'),
    path('sellers/<int:id>/', DetailSellerView.as_view(), name='sellers-detail'),
]

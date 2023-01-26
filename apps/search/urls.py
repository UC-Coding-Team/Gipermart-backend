from django.urls import path
from .views import ProductsSearchView

urlpatterns = [
    path('api/products/search/', ProductsSearchView.as_view(), name='products-search'),
]
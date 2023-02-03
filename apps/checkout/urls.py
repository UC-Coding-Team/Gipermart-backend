from django.urls import path
from .views import OrderList, OrderDetail

urlpatterns = [
    path('checkout/', OrderList.as_view(), name='order-list'),
    path('checkout/<int:pk>/', OrderDetail.as_view(), name='order-detail'),
]

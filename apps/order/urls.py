from django.urls import path
from .views import OrderListCreateAPIView, OrderDetailView, OrderItemListCreateAPIView, OrderItemDetailView

app_name = 'order'

urlpatterns = [
    path('orders/', OrderListCreateAPIView.as_view(), name='order-list'),
    path('orders/<int:pk>/', OrderDetailView.as_view(), name='order-detail'),
    path('orders/<int:order_pk>/items/', OrderItemListCreateAPIView.as_view(), name='order-item-list'),
    path('orders/<int:order_pk>/items/<int:pk>/', OrderItemDetailView.as_view(), name='order-item-detail'),
]
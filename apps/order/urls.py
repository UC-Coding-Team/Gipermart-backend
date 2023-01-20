from django.urls import path
from .views import (

    OrdersViewSet,
    OrderItemViewSet
)


urlpatterns = (

    path('orders/', OrdersViewSet.orders_view(), name='orders'),
    path('orders/create', OrdersViewSet.orders_create_view(), name='orders_create'),
    path('order/<int:pk>', OrdersViewSet.order_view(), name='order'),

    path('order_items/', OrderItemViewSet.order_items_view(), name='order_items'),
    path('order_item/<int:pk>', OrderItemViewSet.order_item_view(), name='order_item'),

)
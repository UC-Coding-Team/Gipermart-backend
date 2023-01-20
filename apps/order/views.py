from rest_framework import viewsets, mixins
from rest_framework import permissions, status
from .models import OrderItem, Order
from .permissions import IsOwner
from .serializers import OrderSerializer, OrderItemSerializer


class OrdersViewSet(viewsets.ModelViewSet):
    """
    Class responsible to process request to Orders
    Provides the following view routes and methods:
        orders_view (get - list)
        orders_create_view (post - create)
        order_view (get - retrieve, put - update)
    """
    # The model object to perform the queries
    queryset = Order.objects.all()
    # The serializer to process the data objects
    serializer_class = OrderSerializer

    @classmethod
    def orders_view(cls):
        cls.permission_classes = (permissions.IsAuthenticated, permissions.IsAdminUser,)
        return cls.as_view({
            'get': 'list'
        })

    @classmethod
    def orders_create_view(cls):
        cls.permission_classes = (permissions.IsAuthenticated, permissions.IsAdminUser,)
        return cls.as_view({
            'post': 'create'
        })

    @classmethod
    def order_view(cls):
        cls.permission_classes = (((permissions.IsAuthenticated & IsOwner) |
                                   (permissions.IsAuthenticated & permissions.IsAdminUser)),)
        return cls.as_view({
            'get': 'retrieve',
            'put': 'update'
        })


class OrderItemViewSet(viewsets.ModelViewSet):
    """
    Class responsible to process Order Items
    Provides the following view routes and methods:
        order_items_view (get - list, post - create)
        order_item_view (get - retrieve, put - update)
    """
    # the model object to perform the queries
    queryset = OrderItem.objects.all()
    # The serializer to process the data objects
    serializer_class = OrderItemSerializer
    # Only allow if authenticated and is owner or if authenticated and is admin

    @classmethod
    def order_items_view(cls):
        return cls.as_view({
            'get': 'list',
            'post': 'create'
        })

    @classmethod
    def order_item_view(cls):
        return cls.as_view({
            'get': 'retrieve',
            'put': 'update'
        })
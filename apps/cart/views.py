from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet

from .models import Cart, CartItem
from rest_framework import generics, mixins
from rest_framework.response import Response
from .serializers import CartSerializer, CartItemSerializer, CartCreateSerializer


class CartViewSet(viewsets.ModelViewSet):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer


# class CartItemViewSet(viewsets.ModelViewSet):
#     queryset = CartItem.objects.all()
#     serializer_class = CartItemSerializer

class ALLCartListAPIView(generics.ListAPIView):
    queryset = CartItem.objects.all()
    serializer_class = CartItemSerializer


class CartAPIView(APIView):
    def get(self, request, pk):
        cart = CartItem.objects.get(user_id=pk)
        serializer = CartItemSerializer(cart, context={'request': request})
        return Response(serializer.data)


class CartCreateAPIView(generics.CreateAPIView):
    queryset = CartItem.objects.all()
    serializer_class = CartCreateSerializer


class CartDeleteAPIView(mixins.DestroyModelMixin, GenericViewSet):
    queryset = CartItem.objects.all()
    serializer_class = CartCreateSerializer

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


class CartUpdateAPIView(generics.RetrieveUpdateAPIView):
    queryset = CartItem.objects.all()
    serializer_class = CartCreateSerializer

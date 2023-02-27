from django.shortcuts import render
from rest_framework import generics
from .models import Checkout
from .serializers import CheckoutSerializer, CheckoutAllSerializer


class CheckoutList(generics.CreateAPIView):
    queryset = Checkout.objects.all()
    serializer_class = CheckoutSerializer


class CheckoutDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Checkout.objects.all()
    serializer_class = CheckoutAllSerializer

class CheckoutDetailAll(generics.ListAPIView):
    queryset = Checkout.objects.all()
    serializer_class = CheckoutAllSerializer

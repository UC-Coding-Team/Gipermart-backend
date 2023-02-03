from django.shortcuts import render
from rest_framework import generics
from .models import Checkout
from .serializers import CheckoutSerializer,CheckoutAllSerializer

class CheckoutList(generics.ListCreateAPIView):
    queryset = Checkout.objects.all()
    serializer_class = CheckoutSerializer

class CheckoutDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Checkout.objects.all()
    serializer_class = CheckoutAllSerializer
from django.urls import path
from .views import CheckoutList, CheckoutDetail

urlpatterns = [
    path('checkout/', CheckoutList.as_view(), name='Checkout-list'),
    path('checkout/<int:pk>/', CheckoutDetail.as_view(), name='Checkout-detail'),
]

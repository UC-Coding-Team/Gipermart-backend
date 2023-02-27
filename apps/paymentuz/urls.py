from django.urls import path

from apps.paymentuz.views import PaymentView


urlpatterns = [
    path('paycom/', PaymentView.as_view())
]
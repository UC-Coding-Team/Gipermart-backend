from django.urls import path

from .views import MerchantAPIView


urlpatterns = [
    path("merchant/", MerchantAPIView.as_view())
]
from django.urls import path

from .views import MerchantAPIView


urlpatterns = [
    path("add/", MerchantAPIView.as_view())
]
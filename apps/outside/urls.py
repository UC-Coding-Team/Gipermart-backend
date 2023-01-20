from django.urls import path, include
from .views import Sliderviews,Stockviews,Brandviews
# from
from rest_framework.routers import DefaultRouter



urlpatterns = [
    # path("", include(router.urls)),
    path("slider/", Sliderviews.as_view(),name="Sliderviews"),
    path("stock/", Stockviews.as_view(), name="Stockviews"),
    path("brand/", Brandviews.as_view(), name="Brandviews"),

]
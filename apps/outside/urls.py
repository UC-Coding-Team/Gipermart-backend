from django.urls import path, include
from .views import Sliderviews,Stockviews
# from
from rest_framework.routers import DefaultRouter



urlpatterns = [
    # path("", include(router.urls)),
    path("slider/api/", Sliderviews.as_view(),name="Sliderviews"),
    path("stock/api/", Stockviews.as_view(), name="Stockviews"),

]
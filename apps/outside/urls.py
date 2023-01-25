from django.urls import path, include
from .views import Sliderviews,Stockviews,Brandviews
# from
from rest_framework.routers import DefaultRouter

router = DefaultRouter()

router.register(r"slider", Sliderviews)
router.register(r"stock", Stockviews)
router.register(r"brand", Brandviews)



urlpatterns = [
    path("", include(router.urls)),
    # path("Add_to_cart/", Add_to_cartviews.as_view(), name="Add_to_cartviews"),

]
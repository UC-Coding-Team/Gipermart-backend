from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()

router.register(r"product-lists", views.ListProductView)

urlpatterns = [
    path("", include(router.urls)),
    path("category/", views.CategoryListAPIView.as_view()),
    path("category/<int:pk>/", views.CategoryAPIView.as_view()),
    path("list/product/", views.ListProductAPIView.as_view()),
    path("product/<int:pk>/delete/", views.DestroyProductAPIView.as_view()),
    path("product/<str:uuid>/", views.ProductDetailView.as_view()),



]
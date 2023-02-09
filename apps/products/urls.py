from django.urls import path
from rest_framework.routers import DefaultRouter

from apps.products.views import CategoryList, ProductByCategory, ProductDetailBySlug, AllProductsView, RatingCreate

app_name = "products"
router = DefaultRouter()
router.register('api/products', AllProductsView, 'products')

urlpatterns = [
    path("category/all/", CategoryList.as_view()),
    path(
        "category/<str:slug>/",
        ProductByCategory.as_view(),
    ),
    path("product-detail/<int:pk>/", ProductDetailBySlug.as_view()),
    # path("api/products/", AllProductsView.as_view()),
    path('ratings/', RatingCreate.as_view(), name='rating-create'),


]
urlpatterns += router.urls

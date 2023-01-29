from django.urls import path

from apps.products.views import CategoryList, ProductByCategory, ProductInventoryById

app_name = "products"

urlpatterns = [
    path("api/category/all/", CategoryList.as_view()),
    path(
        "api/products/category/<str:query>/",
        ProductByCategory.as_view(),
    ),
    path("api/<int:query>/", ProductInventoryById.as_view()),

]

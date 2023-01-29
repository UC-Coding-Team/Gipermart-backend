# from django.urls import path, include
# from rest_framework.routers import DefaultRouter
# from . import views
#
# router = DefaultRouter()
#
# router.register(r'wishlists', views.WishlistViewSet)
# router.register(r'categories', views.CategoryViewSet)
# router.register(r'products', views.ProductViewSet)
#
# urlpatterns = [
#     path("", include(router.urls)),
# ]


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

from rest_framework.routers import DefaultRouter
from django.urls import path, include
from . import views

router = DefaultRouter()

router.register(r'categories', views.CategoryViewSet, basename='category')
router.register(r'products', views.ProductViewSet, basename='product')
# router.register(r'colors', views.ColorViewSet, basename='color')
# router.register(r'sizes', views.SizeViewSet, basename='size')
# router.register(r'variants', views.VariantViewSet, basename='variant')
router.register(r'sliders', views.SliderViewSet, basename='slider')
router.register(r'stocks', views.StockViewSet, basename='stock')
router.register(r'brands', views.BrandViewSet, basename='brand')

urlpatterns = [
    path('', include(router.urls)),
]
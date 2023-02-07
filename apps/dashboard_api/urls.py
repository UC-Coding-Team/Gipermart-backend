from rest_framework.routers import DefaultRouter
from django.urls import path, include
from . import views

router = DefaultRouter()

router.register(r'product-stocks', views.ProductStockViewSet, basename='product-stock'),
router.register(r'product-attribute-values', views.ProductAttributeValuesViewSet, basename='product-attribute-values'),
router.register(r'product-attribute-value', views.ProductAttributeValueViewSet, basename='product-attribute-value'),
router.register(r'wish-lists', views.WishlistViewSet, basename='wish-list'),
router.register(r'product-inventors', views.ProductInventoryViewSet, basename='product-inventory'),
router.register(r'product-media', views.MediaViewSet, basename='media'),
router.register(r'product-attribute', views.ProductAttributeViewSet, basename='product-attribute'),
router.register(r'product-type', views.ProductTypeViewSet, basename='product-type'),
router.register(r'product-brand', views.BrandProductViewSet, basename='product-brand'),
router.register(r'product-type-attribute', views.ProductTypeAttributeViewSet, basename='product-type-attribute'),
router.register(r'categories', views.CategoryViewSet, basename='category')
router.register(r'products', views.ProductViewSet, basename='product')
router.register(r'sliders', views.SliderViewSet, basename='slider')
router.register(r'stocks', views.StockViewSet, basename='stock')
router.register(r'brands', views.BrandViewSet, basename='brand')

urlpatterns = [
    path('', include(router.urls)),
]
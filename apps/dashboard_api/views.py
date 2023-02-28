from django.contrib.auth import login
from django.db.models import Sum, Q, DecimalField
from django.db.models.functions import Cast
from django.utils import timezone
from rest_framework import viewsets, status
from rest_framework.decorators import api_view
from rest_framework.filters import SearchFilter
from rest_framework.generics import UpdateAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from . import serializers
from apps.products.models import (
    Category, Product, Brand,
    ProductAttribute, ProductType,
    ProductAttributeValue, ProductInventory,
    Media, Stock, ProductAttributeValues, ProductTypeAttribute,
    Wishlist,
)
from .models import SiteSettings
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from apps.outside import models
from .serializers import SiteSettingsSerializers, PhoneSiteSettingsSerializers, ChangePasswordSerializer, \
    UserLoginSerializer, SellingStatusSerializer
from ..cart.serializers import DashUserSerializer
from ..checkout.models import Checkout
from ..checkout.serializers import CheckoutSerializer


class ProductStockViewSet(viewsets.ModelViewSet):
    queryset = Stock.objects.all()
    serializer_class = serializers.StockProductSerializers
    permission_classes = [AllowAny]


class ProductAttributeValuesViewSet(viewsets.ModelViewSet):
    queryset = ProductAttributeValues.objects.all()
    serializer_class = serializers.ProductAttributeValuesSerializers
    permission_classes = [AllowAny]


class ProductTypeAttributeViewSet(viewsets.ModelViewSet):
    queryset = ProductTypeAttribute.objects.all()
    serializer_class = serializers.ProductTypeAttributeSerializers
    permission_classes = [AllowAny]


class ProductAttributeValueViewSet(viewsets.ModelViewSet):
    queryset = ProductAttributeValue.objects.all()
    serializer_class = serializers.ProductAttributeValueSerializers
    permission_classes = [AllowAny]


class WishlistViewSet(viewsets.ModelViewSet):
    queryset = Wishlist.objects.all()
    serializer_class = serializers.WishlistSerializers
    permission_classes = [AllowAny]


class ProductInventoryViewSet(viewsets.ModelViewSet):
    queryset = ProductInventory.objects.all()
    serializer_class = serializers.ProductInventorySerializers
    permission_classes = [AllowAny]
    filter_backends = [SearchFilter]
    search_fields = ['sku', ]


class MediaViewSet(viewsets.ModelViewSet):
    queryset = Media.objects.all()
    serializer_class = serializers.MediaSerializers
    permission_classes = [AllowAny]


class ProductAttributeViewSet(viewsets.ModelViewSet):
    queryset = ProductAttribute.objects.all()
    serializer_class = serializers.ProductAttributeSerializers
    permission_classes = [AllowAny]
    filter_backends = [SearchFilter]
    search_fields = ['id', 'name']


class ProductTypeViewSet(viewsets.ModelViewSet):
    queryset = ProductType.objects.all()
    serializer_class = serializers.ProductTypeSerializers
    permission_classes = [AllowAny]
    filter_backends = [SearchFilter]
    search_fields = ['id', 'name']


class BrandProductViewSet(viewsets.ModelViewSet):
    queryset = Brand.objects.all()
    serializer_class = serializers.ProductBrandSerializers
    permission_classes = [AllowAny]
    filter_backends = [SearchFilter]
    search_fields = ['id', 'name']


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = serializers.CategorySerializers
    permission_classes = [AllowAny]
    filter_backends = [SearchFilter]
    search_fields = ['id', 'name']


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = serializers.ProductSerializers
    permission_classes = [AllowAny]
    filter_backends = [SearchFilter]
    search_fields = ['id', 'name']


class SliderViewSet(viewsets.ModelViewSet):
    queryset = models.Slider.objects.all()
    serializer_class = serializers.SliderSerializers
    permission_classes = [AllowAny]
    filter_backends = [SearchFilter]
    search_fields = ['id', 'slug']


class StockViewSet(viewsets.ModelViewSet):
    queryset = models.Stock.objects.all()
    serializer_class = serializers.StockSerializers
    permission_classes = [AllowAny]
    filter_backends = [SearchFilter]
    search_fields = ['id', 'slug']


class BrandViewSet(viewsets.ModelViewSet):
    queryset = models.Brand.objects.all()
    serializer_class = serializers.BrandSerializers
    permission_classes = [AllowAny]
    filter_backends = [SearchFilter]
    search_fields = ['id', 'slug']


class UsersViewSet(viewsets.ModelViewSet):
    queryset = models.User.objects.all()
    serializer_class = DashUserSerializer
    permission_classes = [AllowAny]
    filter_backends = [SearchFilter]
    search_fields = ['id', 'slug']


class CheckoutViewSet(viewsets.ModelViewSet):
    queryset = Checkout.objects.all()
    serializer_class = CheckoutSerializer
    permission_classes = [AllowAny]
    filter_backends = [SearchFilter]
    search_fields = ['id', 'slug']


class SiteSettingsViewSet(viewsets.ModelViewSet):
    queryset = SiteSettings.objects.all()
    serializer_class = SiteSettingsSerializers
    permission_classes = [AllowAny]


class PhoneSiteSettingsViewSet(viewsets.ModelViewSet):
    queryset = SiteSettings.objects.all()
    serializer_class = PhoneSiteSettingsSerializers
    permission_classes = [AllowAny]


class UserLoginView(APIView):
    """
    A view that handles user login requests.
    """

    def post(self, request):
        """
        Handle POST requests to the view.
        """
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            login(request, user)
            return Response({"message": "Login successful."}, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ChangePasswordView(UpdateAPIView):
    serializer_class = ChangePasswordSerializer
    permission_classes = [AllowAny]

    def get_object(self):
        return self.request.user

    def update(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            old_password = serializer.data.get('old_password')
            if not self.object.check_password(old_password):
                return Response({'old_password': ['Wrong password.']}, status=status.HTTP_400_BAD_REQUEST)

            self.object.set_password(serializer.data.get('new_password'))
            self.object.save()
            return Response({'status': 'password set'}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def selling_status(request):
    """
    A view that returns the selling status for the current day.

    The selling status includes the number of checkouts, the total sum of all checkouts,
    and the last 10 checkouts sorted by creation date.
    """
    # Get checkouts that are paid and have next status

    today = timezone.now()
    checkout_items = Checkout.objects.filter(Q(PAY_STATUS=True) | Q(NAXT_STATUS=True), created_at__date=today)
    # checkout_items_total = checkout_items.aggregate(total_price=Sum('cart__total'))['total_price'] or 0
    checkout_items_total = checkout_items.annotate(
        total_decimal=Cast('cart__total', output_field=DecimalField())
    ).aggregate(total_price=Sum('total_decimal'))['total_price'] or 0
    checkout_list = Checkout.objects.filter(Q(PAY_STATUS=True) | Q(NAXT_STATUS=True)).order_by('-created_at')[:10]

    # Calculate total checkout items and total checkout price
    data = {
        'checkout_count': checkout_items.aggregate(total=Sum('cart__quantity')).get('total') or 0,
        'total_sum': checkout_items_total,
        'checkout_list': checkout_list
    }

    # Serialize the data
    serializer = SellingStatusSerializer(data)

    # Return the response
    return Response(serializer.data)
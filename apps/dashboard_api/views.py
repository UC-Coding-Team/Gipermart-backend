from django.db.models import Sum, Q, DecimalField
from django.db.models.functions import Cast
from django.utils import timezone
from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.filters import SearchFilter
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from django.core.mail import send_mail
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model
from .serializers import LoginSerializer, ChangePasswordSerializer, ForgetPasswordSerializer
from . import serializers as serial
from apps.products.models import (
    Category, Product, Brand,
    ProductAttribute, ProductType,
    ProductAttributeValue, ProductInventory,
    Media, Stock, ProductAttributeValues, ProductTypeAttribute,
    Wishlist,
)
from rest_framework import serializers
from .models import SiteSettings
from rest_framework.permissions import AllowAny
from apps.outside import models
from .serializers import SiteSettingsSerializers, PhoneSiteSettingsSerializers, \
    SellingStatusSerializer
from ..cart.serializers import DashUserSerializer
from ..checkout.models import Checkout
from ..checkout.serializers import CheckoutSerializer

User = get_user_model()


class ProductStockViewSet(viewsets.ModelViewSet):
    queryset = Stock.objects.all()
    serializer_class = serial.StockProductSerializers
    permission_classes = [AllowAny]


class ProductAttributeValuesViewSet(viewsets.ModelViewSet):
    queryset = ProductAttributeValues.objects.all()
    serializer_class = serial.ProductAttributeValuesSerializers
    permission_classes = [AllowAny]


class ProductTypeAttributeViewSet(viewsets.ModelViewSet):
    queryset = ProductTypeAttribute.objects.all()
    serializer_class = serial.ProductTypeAttributeSerializers
    permission_classes = [AllowAny]


class ProductAttributeValueViewSet(viewsets.ModelViewSet):
    queryset = ProductAttributeValue.objects.all()
    serializer_class = serial.ProductAttributeValueSerializers
    permission_classes = [AllowAny]


class WishlistViewSet(viewsets.ModelViewSet):
    queryset = Wishlist.objects.all()
    serializer_class = serial.WishlistSerializers
    permission_classes = [AllowAny]


class ProductInventoryViewSet(viewsets.ModelViewSet):
    queryset = ProductInventory.objects.all()
    serializer_class = serial.ProductInventorySerializers
    permission_classes = [AllowAny]
    filter_backends = [SearchFilter]
    search_fields = ['sku', ]


class MediaViewSet(viewsets.ModelViewSet):
    queryset = Media.objects.all()
    serializer_class = serial.MediaSerializers
    permission_classes = [AllowAny]


class ProductAttributeViewSet(viewsets.ModelViewSet):
    queryset = ProductAttribute.objects.all()
    serializer_class = serial.ProductAttributeSerializers
    permission_classes = [AllowAny]
    filter_backends = [SearchFilter]
    search_fields = ['id', 'name']


class ProductTypeViewSet(viewsets.ModelViewSet):
    queryset = ProductType.objects.all()
    serializer_class = serial.ProductTypeSerializers
    permission_classes = [AllowAny]
    filter_backends = [SearchFilter]
    search_fields = ['id', 'name']


class BrandProductViewSet(viewsets.ModelViewSet):
    queryset = Brand.objects.all()
    serializer_class = serial.ProductBrandSerializers
    permission_classes = [AllowAny]
    filter_backends = [SearchFilter]
    search_fields = ['id', 'name']


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = serial.CategorySerializers
    permission_classes = [AllowAny]
    filter_backends = [SearchFilter]
    search_fields = ['id', 'name']


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = serial.ProductSerializers
    permission_classes = [AllowAny]
    filter_backends = [SearchFilter]
    search_fields = ['id', 'name']


class SliderViewSet(viewsets.ModelViewSet):
    queryset = models.Slider.objects.all()
    serializer_class = serial.SliderSerializers
    permission_classes = [AllowAny]
    filter_backends = [SearchFilter]
    search_fields = ['id', 'slug']


class StockViewSet(viewsets.ModelViewSet):
    queryset = models.Stock.objects.all()
    serializer_class = serial.StockSerializers
    permission_classes = [AllowAny]
    filter_backends = [SearchFilter]
    search_fields = ['id', 'slug']


class BrandViewSet(viewsets.ModelViewSet):
    queryset = models.Brand.objects.all()
    serializer_class = serial.BrandSerializers
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


class LoginView(TokenObtainPairView):
    serializer_class = LoginSerializer


class ChangePasswordView(APIView):
    permission_classes = (IsAuthenticated, IsAdminUser)
    serializer_class = ChangePasswordSerializer

    def put(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'detail': _('Password changed successfully.')})


class ForgetPasswordView(APIView):
    serializer_class = ForgetPasswordSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            user = User.objects.get(phone_number=serializer.validated_data['phone_number'])
        except User.DoesNotExist:
            msg = _('User with provided phone number does not exist.')
            raise serializers.ValidationError(msg, code='authorization')
        new_password = User.objects.make_random_password()
        user.set_password(new_password)
        user.save()
        send_mail(
            _('Your new password'),
            _('Your new password is: ') + new_password,
            settings.DEFAULT_FROM_EMAIL,
            [user.email],
            fail_silently=False,
        )
        return Response({'detail': _('Your new password has been sent to your email.')})

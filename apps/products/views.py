import logging

from rest_framework import viewsets, status
from rest_framework.exceptions import NotAcceptable, PermissionDenied
from rest_framework.response import Response
# from django_filters import filters
from rest_framework.generics import ListAPIView, RetrieveAPIView, DestroyAPIView, get_object_or_404
from rest_framework.views import APIView

from .permission import ModelViewSetsPermission, IsOwnerAuth
from .serializers import CategoryListSerializer, ProductSerializer, CreateProductSerializer, ProductDetailSerializer
# from django_filters.rest_framework import DjangoFilterBackend
from .models import Category, Product
from googletrans import Translator

translator = Translator()
logger = logging.getLogger(__name__)


class CategoryListAPIView(ListAPIView):
    # permission_classes = [permissions.IsAuthenticated]
    serializer_class = CategoryListSerializer
    # filter_backends = (
    #     DjangoFilterBackend,
    #     filters.SearchFilter,
    #     filters.OrderingFilter,
    # )
    search_fields = ("title",)
    ordering_fields = ("create_at",)
    filter_fields = ("create_at",)

    # queryset = Category.objects.all()

    def get_queryset(self):
        queryset = Category.objects.all()
        return queryset


class CategoryAPIView(RetrieveAPIView):
    # permission_classes = [permissions.IsAuthenticated]
    serializer_class = CategoryListSerializer
    queryset = Category.objects.all()

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        data = {}
        for k, v in serializer.data.items():
            data[k] = translator.translate(str(v), dest="ar").text

        return Response(data)


class ListProductAPIView(ListAPIView):
    serializer_class = ProductSerializer
    # filter_backends = (
    #     DjangoFilterBackend,
    #     filters.SearchFilter,
    #     filters.OrderingFilter,
    # )
    search_fields = ("title",)
    ordering_fields = ("create_at",)
    # filter_fields = ("views",)
    queryset = Product.objects.all()

    # def get_queryset(self):
    #     import cProfile
    #     from django.contrib.auth.models import User
    #     u = User.objects.get(id=5)
    #     p = Product.objects.create(seller=u, category=Category.objects.get(id=1), title='test', price=20, description='dsfdsfdsf', quantity=10)
    #     cProfile.runctx('for i in range(5000): ProductSerializer(p).data', globals(), locals(), sort='tottime')
    #     queryset = Product.objects.all()
    #     return queryset

    # @time_calculator
    def time(self):
        return 0

    # Cache requested url for each user for 2 hours
    # @method_decorator(cache_page(60 * 60 * 2))
    # @method_decorator(vary_on_cookie)
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        self.time()
        return Response(serializer.data)


class ListProductView(viewsets.ModelViewSet):
    permission_classes = (ModelViewSetsPermission,)
    serializer_class = CreateProductSerializer
    http_method_names = ("get",)
    # filter_backends = (
    #     DjangoFilterBackend,
    #     filters.SearchFilter,
    #     filters.OrderingFilter,
    # )
    search_fields = ("title",)
    ordering_fields = ("create_at",)
    # filter_fields = ("views",)
    queryset = Product.objects.all()

    # def list(self, request, *args, **kwargs):
    #     queryset = self.filter_queryset(self.get_queryset())
    #     print("queryset -> ", queryset)
    #     serializer = self.get_serializer(queryset, many=True)
    #     return Response(serializer)

    def update(self, request, *args, **kwargs):
        from django.contrib.auth.models import User

        if User.objects.get(username="admin") != self.get_object().seller:
            raise NotAcceptable("you don't own product")
        return super(ListProductView, self).update(request, *args, **kwargs)


class DestroyProductAPIView(DestroyAPIView):
    permission_classes = [IsOwnerAuth]
    serializer_class = ProductDetailSerializer
    queryset = Product.objects.all()

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.is_deleted = True
        instance.save()
        return Response({"detail": "Product deleted"})


class ProductDetailView(APIView):
    def get(self, request, uuid):
        product = Product.objects.get(uuid=uuid)
        x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
        if x_forwarded_for:
            ip = x_forwarded_for.split(",")[0]
        else:
            ip = request.META.get("REMOTE_ADDR")

            # if not ProductViews.objects.filter(product=product, ip=ip).exists():
            #     ProductViews.objects.create(product=product, ip=ip)

            product.views += 1
            product.save()
        serializer = ProductDetailSerializer(product, context={"request": request})

        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        user = request.user
        product = get_object_or_404(Product, pk=pk)
        if product.user != user:
            raise PermissionDenied("this product don't belong to you.")

        serializer = ProductDetailSerializer(
            product, data=request.data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

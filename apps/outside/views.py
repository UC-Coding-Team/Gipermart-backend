from rest_framework import viewsets
from .models import Slider,Stock,Brand
from .serializers import Slider_serializer,Stock_serializer,Brand_serializer
from ..products.permission import ModelViewSetsPermission


class Sliderviews(viewsets.ModelViewSet):
    permission_classes = (ModelViewSetsPermission,)
    serializer_class = Slider_serializer
    queryset = Slider.objects.all()
    http_method_names = ("get",)


class Stockviews(viewsets.ModelViewSet):
    permission_classes = (ModelViewSetsPermission,)
    serializer_class = Stock_serializer
    queryset = Stock.objects.all()
    http_method_names = ("get",)


class Brandviews(viewsets.ModelViewSet):
    permission_classes = (ModelViewSetsPermission,)
    serializer_class = Brand_serializer
    queryset = Brand.objects.all()
    http_method_names = ("get",)


# class Add_to_cartviews(APIView):
#     serializer_class = Add_to_cart_serializer
#
#
#
#     def get(self, request, format=None):
#         transformers = Add_to_cart.objects.all()
#         serializer = Brand_serializer(transformers, many=True)
#         return Response(serializer.data)
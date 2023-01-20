from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Slider,Stock,Brand
from .serializers import Slider_serializer,Stock_serializer,Brand_serializer


class Sliderviews(APIView):
    serializer_class = Slider_serializer

    def get(self, request, format=None):
        transformers = Slider.objects.all()
        serializer = Slider_serializer(transformers, many=True)
        return Response(serializer.data)

class Stockviews(APIView):
    serializer_class = Stock_serializer

    def get(self, request, format=None):
        transformers = Stock.objects.all()
        serializer = Stock_serializer(transformers, many=True)
        return Response(serializer.data)

class Brandviews(APIView):
    serializer_class = Stock_serializer

    def get(self, request, format=None):
        transformers = Brand.objects.all()
        serializer = Brand_serializer(transformers, many=True)
        return Response(serializer.data)
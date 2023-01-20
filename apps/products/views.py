import logging
from rest_framework.response import Response
from django_filters import filters
from rest_framework.generics import ListAPIView, RetrieveAPIView
from .serializers import CategoryListSerializer
from django_filters.rest_framework import DjangoFilterBackend
from .models import Category
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
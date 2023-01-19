from rest_framework import serializers
from .models import Slider,Stock

class Slider_serializer(serializers.ModelSerializer):
    class Meta:
        model = Slider
        fields = ['id','images','created_at','updated_at']

class Stock_serializer(serializers.ModelSerializer):
    class Meta:
        model = Stock
        fields = ['id','slug','images','created_at','updated_at']
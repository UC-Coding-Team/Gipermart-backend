from rest_framework import serializers
from .models import Slider,Stock,Brand

class Slider_serializer(serializers.ModelSerializer):
    class Meta:
        model = Slider
        fields = ['id','images','created_at','updated_at']

class Stock_serializer(serializers.ModelSerializer):
    class Meta:
        model = Stock
        fields = ['id','slug','images','created_at','updated_at']

class Brand_serializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = ["id","slug","images","category","product","created_at","updated_at"]


# class Add_to_cart_serializer(serializers.ModelSerializer):
#     class Meta:
#         model = Add_to_cart
#         fields = ["id","product","user","created_at","updated_at"]
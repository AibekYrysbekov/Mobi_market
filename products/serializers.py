from rest_framework import serializers
from .models import Product, LikeProduct


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ('id', 'name', 'description', 'available', 'photo', 'short_description', 'price')


class LikeProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = LikeProduct
        fields = ('user', 'product', 'like')

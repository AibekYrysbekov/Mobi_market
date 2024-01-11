from rest_framework import serializers
from .models import Product, LikeProduct, ProductPhoto


class ProductPhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductPhoto
        fields = ('id', 'photo')


class ProductSerializer(serializers.ModelSerializer):
    photos = ProductPhotoSerializer(many=True, required=False)

    class Meta:
        model = Product
        fields = ('id', 'name', 'description', 'short_description', 'available', 'price', 'photos')

    def create(self, validated_data):
        photos_data = validated_data.pop('photos', [])

        product = Product.objects.create(**validated_data)
        for photo_data in photos_data:
            ProductPhoto.objects.create(product=product, photo=photo_data)

        return product


class LikeProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = LikeProduct
        fields = ('user', 'product', 'like')

from rest_framework import viewsets, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Product, ProductPhoto
from .serializers import ProductSerializer
from .utils import get_like, delete_like, get_like_count


class ProductCreateApiView(viewsets.ModelViewSet):
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Product.objects.all().filter(created_by=self.request.user)

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    def create(self, request, *args, **kwargs):
        photos_data = request.data.pop('photos', [])
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            product = serializer.save(created_by=request.user)

            for photo_data in photos_data:
                ProductPhoto.objects.create(product=product, photo=photo_data)

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def like_product(request, product_id):
    user = request.user

    try:
        product = Product.objects.get(id=product_id)
    except Product.DoesNotExist:
        return Response({"error": "Product does not exist"}, status=status.HTTP_404_NOT_FOUND)

    if get_like(user, product):
        return Response({"message": "Product liked successfully"}, status=status.HTTP_201_CREATED)
    else:
        return Response({"message": "Product already liked"}, status=status.HTTP_200_OK)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def unlike_product(request, product_id):
    user = request.user

    try:
        product = Product.objects.get(id=product_id)
    except Product.DoesNotExist:
        return Response({"error": "Product does not exist"}, status=status.HTTP_404_NOT_FOUND)

    if delete_like(user, product):
        return Response({"message": "Product unliked successfully"}, status=status.HTTP_200_OK)
    else:
        return Response({"message": "Product is not liked"}, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([])
def get_like_counts(request, product_id):
    like_counts = get_like_count(product_id)
    return Response(like_counts, status=status.HTTP_200_OK)

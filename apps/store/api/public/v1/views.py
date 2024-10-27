from rest_framework import generics

from apps.store.api.public.v1.serializers import (
    ProductSerializer,
    CategorySerializer,
)
from apps.store.models import (
    Product,
    Category
)


class ProductListAPIView(generics.ListAPIView):
    serializer_class = ProductSerializer
    queryset = Product.objects.all().order_by('-id')


class CategoryListAPIView(generics.ListAPIView):
    serializer_class = CategorySerializer
    queryset = Category.objects.all().order_by('-name')

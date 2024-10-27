from rest_framework import generics

from apps.store.api.public.v1.serializers import (
    ProductSerializer
)
from apps.store.models import Product


class ProductListAPIView(generics.ListAPIView):
    serializer_class = ProductSerializer
    queryset = Product.objects.all().order_by('-id')

from rest_framework.response import Response
from rest_framework import status, generics

from apps.store.api.public.v1.serializers import (
    ProductSerializer,
    CategorySerializer,
    SimilarProductSerializer,
)
from apps.store.models import Product, Category
from apps.store.utils import get_similar_objects


class ProductListAPIView(generics.ListAPIView):
    serializer_class = ProductSerializer
    queryset = Product.objects.all().order_by('-id')


class CategoryListAPIView(generics.ListAPIView):
    serializer_class = CategorySerializer
    queryset = Category.objects.all().order_by('-name')


class SimilarProductCreateAPIView(generics.CreateAPIView):
    serializer_class = SimilarProductSerializer
    queryset = Product.objects.none()

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        products, result = get_similar_objects(
            query=data.get('query'),
            add_condition=data.get('add_condition'),
            product_category=data.get('category_name'),
            same_category=data.get('same_category'),
            n=data.get('n_results'),
        )

        serializer = ProductSerializer(products, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

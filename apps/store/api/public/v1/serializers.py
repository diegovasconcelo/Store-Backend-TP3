from rest_framework import serializers


from apps.store.models import (
    Product,
    SubCategory,
    Category,
)


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'
        depth = 1


class SubCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = SubCategory
        fields = ('id', 'name', 'description')


class CategorySerializer(serializers.ModelSerializer):
    subcategories = SubCategorySerializer(
        many=True,
        read_only=True,
        source='subcategory_set'
    )

    class Meta:
        model = Category
        fields = ('id', 'name', 'description', 'subcategories')


class SimilarProductSerializer(serializers.Serializer):
    query = serializers.CharField()
    add_condition = serializers.BooleanField(default=False)
    same_category = serializers.BooleanField(default=True)
    category_name = serializers.CharField(required=False)
    n_results = serializers.IntegerField(min_value=1, max_value=10)

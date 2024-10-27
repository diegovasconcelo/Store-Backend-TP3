from django.urls import path

from apps.store.api.public.v1.views import (
    ProductListAPIView,
    CategoryListAPIView,
    SimilarProductCreateAPIView,
)


urlpatterns = [
    path(
        'products/',
        ProductListAPIView.as_view(),
        name='product-list'
    ),
    path(
        'products/categories/',
        CategoryListAPIView.as_view(),
        name='category-list'
    ),
    path(
        'products/similar/',
        SimilarProductCreateAPIView.as_view(),
        name='product-similar'
    ),
]

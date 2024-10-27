from django.urls import path

from apps.store.api.public.v1.views import (
    ProductListAPIView,
    CategoryListAPIView,
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
]

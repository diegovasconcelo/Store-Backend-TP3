from django.urls import path

from apps.store.api.public.v1.views import (
    ProductListAPIView,
)


urlpatterns = [
    path(
        'products/',
        ProductListAPIView.as_view(),
        name='product-list'
    ),
]

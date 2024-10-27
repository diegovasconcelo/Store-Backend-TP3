from django.urls import path, include

urlpatterns = [
    path('api/public/v1/', include('apps.store.api.public.v1.urls')),
]

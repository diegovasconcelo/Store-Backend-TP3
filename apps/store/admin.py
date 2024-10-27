from django.contrib import admin

from apps.store.models import (
    Category,
    Client,
    Product,
    Recommendation,
    RecommendationItem,
    Sale,
    Store,
    SubCategory
)


admin.site.register(Category)
admin.site.register(Client)
admin.site.register(Product)
admin.site.register(Recommendation)
admin.site.register(RecommendationItem)
admin.site.register(Sale)
admin.site.register(Store)
admin.site.register(SubCategory)

from django.core.management.base import BaseCommand

from apps.store.models import Product
from apps.store.recommendations.recommendation_service import upsert_product


class Command(BaseCommand):
    help = 'Populate vectors for products'

    def handle(self, *args, **options):
        products = Product.objects.all()
        total = 0
        for product in products:
            metadata = {
                'category': product.category.name,
                'subcategory': product.subcategory.name,
            }

            upsert_product(product.name, product.id, metadata)
            self.stdout.write(
                self.style.SUCCESS(f'Product {product.name} added to vectors')
            )
            total += 1

        self.stdout.write(self.style.SUCCESS(f'Total products added: {total}'))

from django.core.management.base import BaseCommand

from apps.store.recommendations.recommendation_service import get_similar


class Command(BaseCommand):
    help = 'Get similar products'

    def handle(self, *args, **options):
        query = input('Enter your query: ')
        product_category = None
        same_category = None
        add_filter = input('Do you want to add a filter? (y/n) ')
        if add_filter.lower() == 'y':
            product_category = input(
                'Enter the product category to filter by: '
            )
            same_category = input(
                'Do you want to get products from the same category? (y/n) '
            )
            same_category = same_category.lower() == 'y'

        result = get_similar(
            query=query,
            add_condition=add_filter,
            prod_category=product_category,
            same_category=same_category,
        )

        self.stdout.write(self.style.SUCCESS(result))

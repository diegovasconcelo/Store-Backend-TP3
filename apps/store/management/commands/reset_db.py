from django.core.management.base import BaseCommand

from apps.store.models import Product, Category, SubCategory
from apps.store.recommendations.chroma_client import reset_collection


class Command(BaseCommand):
    help = 'Restore the database to its initial state | IRREVERSIBLE ACTION'

    def handle(self, *args, **options):
        self.stdout.write(
            self.style.WARNING(
                'This action will delete all the data in the database.'
            )
        )
        input_text = input('Type "yes" to continue: ')
        if input_text.lower() != 'yes':
            self.stdout.write(self.style.ERROR('Action aborted'))
            return
        self.stdout.write(
            self.style.WARNING(
                'Deleting all data in the database...'
            )
        )
        Category.objects.all().delete()
        SubCategory.objects.all().delete()
        Product.objects.all().delete()
        self.stdout.write(
            self.style.WARNING(
                'Deleting all data in the recommendation database...'
            )
        )
        reset_collection()
        self.stdout.write(self.style.SUCCESS('Database restored successfully'))

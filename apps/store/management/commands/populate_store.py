import random
import json
from decimal import Decimal

from django.core.management.base import BaseCommand
from django.db import transaction

from faker import Faker

from apps.store.models import (
    Sale,
    Store,
    Client,
    Product,
    Category,
    SubCategory,
    PaymentMethod,
)

fake = Faker()

CATEGORIES_DATA = {
    'Climatization': {
        'description': 'Category for all climatization products',
        'subcategories': {
            'Air Conditioners': {
                'description': 'Category for all air conditioners'
            },
            'Heaters': {'description': 'Category for all heaters'},
            'Fans': {'description': 'Category for all fans'}
        }
    },
    "Electronics": {
        "description": "Category for all electronic products",
        "subcategories": {
            "Smartphones": {"description": "Category for all smartphones"},
            "Laptops": {"description": "Category for all laptops"},
            "Tablets": {"description": "Category for all tablets"}
        }
    },
    "Audio & Video": {
        "description": "Category for all audio and video products",
        "subcategories": {
            "Headphones": {"description": "Category for all headphones"},
            "Speakers": {"description": "Category for all speakers"},
            "Televisions": {"description": "Category for all televisions"},
            "Cables": {"description": "Category for all cables"}
        }
    },
    "Clothing": {
        "description": "Category for all clothing products",
        "subcategories": {
            "T-Shirts": {"description": "Category for all t-shirts"},
            "Pants": {"description": "Category for all pants"},
            "Shoes": {"description": "Category for all shoes"}
        }
    },
    "Books": {
        "description": "Category for all book products",
        "subcategories": {
            "Fiction": {"description": "Category for all fiction books"},
            "Textbooks": {"description": "Category for all textbooks"},
            "eBooks": {"description": "Category for all ebooks"}
        }
    },
    "Home & Garden": {
        "description": "Category for all home and garden products",
        "subcategories": {
            "Furniture": {"description": "Category for all furniture"},
            "Tools": {"description": "Category for all tools"},
            "Plants": {"description": "Category for all plants"}
        }
    },
    "Gamming": {
        "description": "Category for all gamming products",
        "subcategories": {
            "Consoles": {"description": "Category for all consoles"},
            "Games": {"description": "Category for all games"},
            "Accessories": {"description": "Category for all accessories"}
        }
    },
    "Sports": {
        "description": "Category for all sports products",
        "subcategories": {
            "Fitness": {"description": "Category for all fitness products"},
            "Clothing": {"description": "Category for all sports clothing"},
            "Equipment": {"description": "Category for all sports equipment"}
        }
    },
    "Photography": {
        "description": "Category for all photography products",
        "subcategories": {
            "Cameras": {"description": "Category for all cameras"},
            "Lenses": {"description": "Category for all lenses"},
            "Accessories": {"description": "Category for all accessories"}
        }
    }
}
PRODUCT_NAMES = {
    "Smartphones": [
        "iPhone 13", "Samsung Galaxy S21", "Google Pixel 6", "OnePlus 9"
    ],
    "Laptops": [
        "MacBook Pro", "Dell XPS 13", "Lenovo ThinkPad", "HP Spectre"
    ],
    "Tablets": [
        "iPad Pro", "Samsung Galaxy Tab", "Microsoft Surface"
    ],
    "Air Conditioners": [
        "Samsung Split", "LG Inverter", "Carrier Window"
    ],
    "Heaters": [
        "Electric Heater Pro", "Gas Heater Plus", "Infrared Heater"
    ],
    "Fans": [
        "Standing Fan Plus", "Ceiling Fan Pro", "Desktop Fan"
    ],
}


class Command(BaseCommand):
    help = 'Populates the database with fake data'

    def add_arguments(self, parser):
        parser.add_argument(
            '--clients',
            type=int,
            default=50,
            help='Number of clients to create'
        )
        parser.add_argument(
            '--products',
            type=int,
            default=100,
            help='Number of products to create'
        )
        parser.add_argument(
            'create-sales',
            type=bool,
            default=False,
            help='Create sales with recommendations the system'
        )
        parser.add_argument(
            '--sales',
            type=int,
            default=200,
            help='Number of sales to create'
        )
        parser.add_argument(
            '--products-file',
            type=str,
            help='Path to a JSON file with products data'
        )

    def create_stores(self):
        stores = []
        store_names = [
            "Main Shop", "Apple Store", "Plaza Central",
            "Tech Store", "Fashion Mall", "Bookstore"
        ]

        for name in store_names:
            store, _ = Store.objects.get_or_create(
                name=name,
                defaults={
                    'description': fake.text(),
                    'local_number': fake.building_number()
                }
            )
            stores.append(store)

        return stores

    def create_categories_and_subcategories(self):
        categories = []
        for cat_name, cat_data in CATEGORIES_DATA.items():
            category, category_created = Category.objects.get_or_create(
                name=cat_name,
                defaults=dict(
                    description=cat_data['description']
                )
            )

            for subcat_name, subcat_data in cat_data['subcategories'].items():
                SubCategory.objects.get_or_create(
                    name=subcat_name,
                    defaults=dict(
                        description=subcat_data['description'],
                        category=category
                    )
                )
            categories.append(category)

        return categories

    def create_clients(self, num_clients):
        clients = []
        for _ in range(num_clients):
            client_name = fake.name()
            client = Client.objects.get_or_create(
                name=client_name,
                email=client_name.lower().replace(' ', '.') + '@store.com',
                defaults=dict(
                    display_name=client_name.title(),
                    phone=fake.phone_number()[0:15],
                    date_of_birth=fake.date_of_birth(
                        minimum_age=18, maximum_age=90
                    ),
                    gender=random.choice(['M', 'F', 'O']),
                    is_active=random.choice([True, True, False]),
                )
            )[0]
            clients.append(client)

        return clients

    def get_product_name(self, subcategory_name):
        if subcategory_name in PRODUCT_NAMES:
            base_name = random.choice(PRODUCT_NAMES[subcategory_name])
            # Add some variation
            if random.random() < 0.5:
                extra = random.choice(['Pro', 'Plus', 'Max', 'Ultra'])
                base_name += f" {extra}"
            if random.random() < 0.3:
                extra = random.choice(['2023', '2024'])
                base_name += f" {extra}"
            return base_name
        return fake.catch_phrase()

    def create_products(self, num_products_per_subcategory):
        products = []
        subcategories = SubCategory.objects.all()

        for subcategory in subcategories:
            category = subcategory.category

            for _ in range(num_products_per_subcategory):
                price_random = Decimal(
                    random.uniform(10.0, 1000.0)
                ).quantize(Decimal('0.01'))
                product = Product.objects.get_or_create(
                    name=self.get_product_name(subcategory.name),
                    defaults=dict(
                        description=fake.text(),
                        price=price_random,
                        stock=random.randint(0, 100),
                        category=category,
                        subcategory=subcategory
                    )
                )[0]
                products.append(product)

        return products

    def create_products_from_file(self, products_data) -> list[Product]:
        products_obj = []
        for product in products_data:
            category, _ = Category.objects.get_or_create(
                name=product['category'],
                defaults=dict(
                    description=fake.text()
                )
            )
            subcategory, _ = SubCategory.objects.get_or_create(
                name=product['subcategory'],
                category=category,
                defaults=dict(
                    description=fake.text()
                )
            )
            product_obj = Product.objects.get_or_create(
                name=product['name'],
                defaults=dict(
                    description=product['short_description'],
                    price=Decimal(product['price']).quantize(Decimal('0.01')),
                    stock=product['stock'],
                    image_url=product.get('image_url'),
                    category=category,
                    subcategory=subcategory,
                )
            )[0]
            products_obj.append(product_obj)

        return products_obj

    def create_sales(self, num_sales, clients, stores, products):
        sales = []
        for _ in range(num_sales):
            # Create sale with products from the same category more often
            client = random.choice(clients)
            category = random.choice(Category.objects.all())
            categ_prod = list(Product.objects.filter(category=category))
            other_products = list(set(products) - set(categ_prod))

            # 70% chance to include products from the same category
            if random.random() < 0.7 and categ_prod:
                num_categ_prod = random.randint(1, min(3, len(categ_prod)))
                sale_products = random.sample(categ_prod, num_categ_prod)

                # Maybe add some products from other categories
                if random.random() < 0.3 and other_products:
                    num_other_products = random.randint(1, 2)
                    sale_products.extend(
                        random.sample(other_products, num_other_products)
                    )
            else:
                num_products = random.randint(1, 5)
                sale_products = random.sample(products, num_products)

            total = sum(product.price for product in sale_products)

            sale = Sale.objects.get_or_create(
                client=client,
                store=random.choice(stores),
                total=total,
                payment_method=random.choice(PaymentMethod.choices)[0]
            )[0]
            sale.products.set(sale_products)

            sales.append(sale)

        return sales

    def read_products_from_file(self, file_path):
        with open(file_path, 'r') as file:
            products_data = json.load(file)
        return products_data

    @transaction.atomic
    def handle(self, *args, **options):
        self.stdout.write('Starting database population...')

        # Create basic data
        stores = self.create_stores()
        self.stdout.write(f'Created {len(stores)} stores')

        if options['products_file']:
            path = options['products_file']
            self.stdout.write('Reading products from file...')
            products_data = self.read_products_from_file(path)
            products = self.create_products_from_file(products_data)
            self.stdout.write(f'Created {len(products_data)} products')
        else:
            categ = self.create_categories_and_subcategories()
            self.stdout.write(
                f'Created {len(categ)} categories with their subcategories'
            )
            products = self.create_products(options['products'])
            self.stdout.write(f'Created {len(products)} products')

        # Create main data
        clients = self.create_clients(options['clients'])
        self.stdout.write(f'Created {len(clients)} clients')

        # Create sales with recommendations
        if options['create-sales']:
            sales = self.create_sales(
                options['sales'], clients, stores, products
            )
            self.stdout.write(
                f'Created {len(sales)} sales with recommendations'
            )

        self.stdout.write(self.style.SUCCESS('Database population complete'))

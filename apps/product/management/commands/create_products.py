from django.core.management.base import BaseCommand
import random
import json
from faker import Faker

from apps.product.models import Category, Product, Order, OrderItem


class Command(BaseCommand):
    help = "Create products tes"

    def handle(self, *args, **options):
        fake = Faker()

        categories = []
        products = []
        orders = []
        order_items = []

        for i in range(1, 11):
            categories.append(
                Category(name=fake.word())
            )
        categories_objs = Category.objects.bulk_create(categories)

        for i in range(1, 151):
            category = random.choice(categories)
            products.append(
                Product(
                    name=fake.word(),
                    price=round(random.uniform(10.00, 500.00), 2),
                    description=fake.text(),
                    stock=random.randint(0, 100),
                    is_active=random.choice([True, False]),
                    attributes={
                        "color": random.choice(['red', 'blue', 'green', 'black', 'white']),
                        "size": random.choice(['S', 'M', 'L', 'XL'])
                    },
                    category=category
            ))
        products_obj = Product.objects.bulk_create(products)

        for i in range(1, 101):
            user_id = random.randint(1, 5)
            orders.append(
                Order(
                    user_id=user_id,
                    status=random.choice(['pending', 'shipping', 'delivered']),
                ))
        orders_obj = Order.objects.bulk_create(orders)

        for i in range(1, 501):
            order = random.choice(orders)
            product = random.choice(products)
            order_items.append(
                OrderItem(
                    order=order,
                    product=product,
                    quantity=random.randint(1, 5)
            ))
        order_items_obj = OrderItem.objects.bulk_create(order_items)
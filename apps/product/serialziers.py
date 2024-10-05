from django.db.models import Sum, Q, F
from rest_framework import serializers

from apps.product.models import Product, Order, OrderItem

from django.contrib.auth import get_user_model

User = get_user_model()


class Task2Serializer(serializers.ModelSerializer):
    last_order = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ("id", "username", "last_order")

    @staticmethod
    def get_last_order(obj):
        data = dict()
        orders = Order.objects.filter(user=obj)

        if orders:
            order = orders.last()
            order_items = OrderItem.objects.filter(order=order)
            data.update({
                "id": order.id,
                "products_count": order_items.count(),
                "total_price": order_items.aggregate(total_price=Sum(F('quantity') * F('product__price')))['total_price'],
                "status": order.status
            })

        return data


class Task3Serializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = "__all__"


class Task4Serializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = "__all__"


class Task5Serializer(serializers.ModelSerializer):
    order_count = serializers.SerializerMethodField()
    order_total_price = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ("id", "username", "order_count", "order_total_price")

    @staticmethod
    def get_order_count(obj):
        return obj.orders.count()

    @staticmethod
    def get_order_total_price(obj):
        orders = obj.orders.all()
        total_price = 0
        for order in orders:
            total_price += order.total_price
        return total_price


class Task6Serializer(serializers.ModelSerializer):
    pass


class Task7Serializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ("id", "status")


class Task8Serializer(serializers.ModelSerializer):
    sales_number = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ("id", "name", "stock", "price", 'sales_number')

    def get_sales_number(self, obj):
        return self.context.get("order_items_count")

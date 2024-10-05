import calendar

from django.db.models import Sum, Q
from django.contrib.auth import get_user_model
from django_filters.rest_framework.backends import DjangoFilterBackend
from django.utils import timezone
from rest_framework.response import Response

from apps.product.models import Product, Order, OrderItem, Category
from apps.product.serialziers import Task2Serializer, Task3Serializer, Task4Serializer, \
    Task5Serializer, Task6Serializer, Task7Serializer, Task8Serializer

from rest_framework.generics import GenericAPIView, ListAPIView, UpdateAPIView

User = get_user_model()


class Task1View(GenericAPIView):
    queryset = Order.objects.all()


class Task2View(ListAPIView):
    queryset = User.objects.all()
    serializer_class = Task2Serializer


class Task3View(ListAPIView):
    queryset = Product.objects.all()
    serializer_class = Task3Serializer

    def get_queryset(self):
        print(self.request.data)
        return Product.objects.filter(attributes__exact=self.request.data)


class Task4View(ListAPIView):
    queryset = Product.objects.all()
    serializer_class = Task4Serializer

    def get_queryset(self):
        return Product.objects.select_related('category').all()


class Task5View(ListAPIView):
    queryset = User.objects.all()
    serializer_class = Task5Serializer

    def get_queryset(self):
        users = User.objects.all()
        data = list()
        for user in users:
            orders = Order.objects.filter(user=user)
            total_price = sum([order.total_price for order in orders])
            if total_price > 60000: # price bazada ko'proq kiritilgani uchun test sifatida 60000 ishlatdim
                data.append(user)

        return data


class Task6View(GenericAPIView):
    queryset = Order.objects.all()
    serializer_class = Task6Serializer

    def get(self, request, *args, **kwargs):
        orders = dict()
        last_year = timezone.now().year

        for month in range(1, 13):
            month_name = calendar.month_name[month]
            order_objs = self.queryset.filter(created_at__year=last_year, created_at__month=month)
            total_price = sum([order.total_price for order in order_objs])
            total_count = order_objs.count()
            orders.update({
                month_name: {
                    "total_price": total_price,
                    "total_count": total_count
                }
            })

        return Response({"data": orders})


class Task8View(GenericAPIView):
    serializer_class = Task8Serializer

    def get(self, request, *args, **kwargs):
        data = list()

        products = Product.objects.filter(stock__lt=10)
        for product in products:
            order_item = OrderItem.objects.filter(product=product)
            if order_item.count() > 3: # bazada sotuvi 10 tadan ko'p productlar bo'lmagani uchun test sifatida 3 ishlatdim
                data.append(self.serializer_class(instance=product, context={"order_items_count": order_item.count()}).data)

        return Response({"data": data})

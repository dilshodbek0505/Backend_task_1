from django.db import models
from django.db.models import Sum, F
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model

from apps.common.models import BaseModel
from apps.product.enums import OrderStatus

User = get_user_model()


class Category(BaseModel):
    name = models.CharField(max_length=256, help_text=_("Product category"))

    def __str__(self):
        return self.name


class Product(BaseModel):
    name = models.CharField(max_length=256, help_text=_("Product name"))
    price = models.DecimalField(max_digits=20, decimal_places=2, default=0, help_text=_("Product price"))
    description = models.TextField(help_text=_("Product description"))
    stock = models.PositiveIntegerField(default=0, help_text=_("Product stock"))
    is_active = models.BooleanField(default=True, help_text=_("Product is active"))
    attributes = models.JSONField(default=dict, help_text=_("Product attributes"))
    category = models.ForeignKey(Category, on_delete=models.PROTECT, null=True, blank=True, help_text=_("Product category"))

    def __str__(self):
        return self.name


class Order(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    status = models.CharField(max_length=20, choices=OrderStatus.get_status(), default='pending')

    def __str__(self):
        return f"{self.user.username} | {self.status}"

    @property
    def total_price(self):
        total_price = OrderItem.objects.filter(order=self).aggregate(total=Sum(F('quantity') * F('product__price')))['total']
        return total_price if total_price is not None else 0


class OrderItem(BaseModel):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.product.name} | {self.quantity}"




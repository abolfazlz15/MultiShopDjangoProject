from django.db import models

from accounts.models import User
from product.models import Product


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    is_paid = models.BooleanField(default=False)

    def __str__(self):
        return self.user.phone


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='items')
    size = models.CharField(max_length=20)
    color = models.CharField(max_length=20)
    quantity  = models.SmallIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.order.user.phone


class DiscountCode(models.Model):
    title = models.CharField(max_length=200, unique=True)
    discount_percent = models.SmallIntegerField(default=0)
    quantity = models.IntegerField(default=0)

    def __str__(self):
        return self.title


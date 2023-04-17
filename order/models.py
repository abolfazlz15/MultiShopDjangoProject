from django.db import models

from accounts.models import User
from product.models import Product
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils.timezone import now

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
    code = models.CharField(max_length=200, unique=True)
    discount_percent = models.SmallIntegerField(
        validators=[
            MinValueValidator(1),
            MaxValueValidator(100),
        ],)
    quantity = models.PositiveIntegerField(default=0, null=True, blank=True)
    allowed_for = models.ManyToManyField(
        User,
        blank=True,
        related_name='coupons',
    )
    valid_from = models.DateTimeField(blank=True, null=True)
    valid_to = models.DateTimeField(blank=True, null=True)
    active = models.BooleanField(
        default=True,
    )
    def __str__(self):
        return self.code

    @staticmethod
    def get(code, user):
        current_time = now()
        coupon_qs = DiscountCode.objects.filter(
            code__exact=code,
            valid_from__lte=current_time,
            valid_to__gte=current_time,
            active=True,
        )
        if not coupon_qs.exists():
            print(1)
            return None
        coupon = coupon_qs.first()
        print(2)
        if coupon.allowed_for.exists() and user not in coupon.allowed_for.all():
            return None
        if coupon.quantity is not None:
            coupon.allowed_for.remove(user)
            coupon.quantity -= 1
            if coupon.quantity <= 0:
                coupon.active = False
            coupon.save()
        return coupon
from django.contrib import admin

from order import models


class OrderItemAdmin(admin.TabularInline):
    model = models.OrderItem


@admin.register(models.Order)
class OrderAdminModel(admin.ModelAdmin):
    list_display = ['user', 'is_paid']
    list_filter = ['is_paid', 'created_at']
    inlines = [OrderItemAdmin]


@admin.register(models.DiscountCode)
class DiscountAdminModel(admin.ModelAdmin):
    list_display = ['title', 'discount_percent', 'quantity']
    search_fields = ['title', 'discount_percent']
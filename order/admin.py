from django.contrib import admin

from order import models

class OrderItemAdmin(admin.TabularInline):
    model = models.OrderItem


@admin.register(models.Order)
class OrderAdminModel(admin.ModelAdmin):
    list_display = ['user', 'phone', 'is_paid']
    list_filter = ['is_paid', 'created_at']
    inlines = [OrderItemAdmin]
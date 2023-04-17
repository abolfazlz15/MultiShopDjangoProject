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
    list_display = ['code', 'discount_percent', 'quantity']
    search_fields = ['code', 'discount_percent']


    def has_module_permission(self, request):
        if not request.user.is_superuser:
            return False
        return True
    
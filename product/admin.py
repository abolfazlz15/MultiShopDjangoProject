from django.contrib import admin
from product.models import Product, Category, ProductColor, ProductSize, ProductImage


admin.site.register(Product)
admin.site.register(Category)
admin.site.register(ProductColor)
admin.site.register(ProductSize)
admin.site.register(ProductImage)

# class PictureInline(modeladmin.StackedInline):
#     model = Picture
# class ProductAdmin(admin.ModelAdmin):
#     inlines = [PictureInline]

# admin.site.register(Product, ProductAdmin)
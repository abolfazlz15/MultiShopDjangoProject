from django.contrib import admin

from product import models

admin.site.register(models.Category)
admin.site.register(models.ProductColor)
admin.site.register(models.ProductSize)
admin.site.register(models.ProductImage)
admin.site.register(models.Comment)
admin.site.register(models.FavoriteProduct)


class InformationProduct(admin.StackedInline):
    model = models.InformationProduct
    extra = 1


class ProductAdminModel(admin.ModelAdmin):
    fields = ['title', 'slug', 'description', 'active_image', 'image', 'price', 'status', 'category', 'color', 'size']
    list_display = ('showImage', 'title', 'price', 'created','status')
    list_display_links = ('showImage', 'title', 'price', 'created')
    list_filter = ['status', 'created', 'updated']
    inlines = [InformationProduct]

    

admin.site.register(models.Product, ProductAdminModel)
admin.site.register(models.InformationProduct)


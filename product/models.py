import os
import uuid

from ckeditor.fields import RichTextField
from django.db import models
from django.urls import reverse
from django.utils.html import format_html
from django.utils.text import slugify

from accounts.models import User
from product.managers import ProductManger


def get_file_path(instance, filename):
    ext = filename.split('.')[-1]
    filename = '%s.%s' % (uuid.uuid4(), ext)
    return os.path.join('product', filename)


class Category(models.Model):
    title = models.CharField(max_length=200)
    parent = models.ForeignKey(
        'self', on_delete=models.SET_NULL, null=True, blank=True, related_name='parents')
    slug = models.SlugField(null=True, blank=True)

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        self.slug = slugify(self.title)
        super(Category, self).save()

    def __str__(self):
        return self.title


class ProductImage(models.Model):
    image = models.ImageField(blank=True, null=True, upload_to=get_file_path)




class ProductColor(models.Model):
    tilte = models.CharField(max_length=50)

    def __str__(self):
        return self.tilte


class ProductSize(models.Model):
    tilte = models.CharField(max_length=10)

    def __str__(self):
        return self.tilte


class Product(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(null=True, blank=True)
    description = RichTextField()
    active_image = models.ImageField(
        blank=True, null=True, upload_to=get_file_path)
    image = models.ManyToManyField(
        ProductImage, verbose_name='images', blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.BooleanField(default=False)
    category = models.ManyToManyField(Category, related_name='videos')
    size = models.ManyToManyField(
        ProductSize, related_name='product_size', blank=True)
    color = models.ManyToManyField(
        ProductColor, related_name='product_color', blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    is_status = ProductManger
    def __str__(self):
        return self.title

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        self.slug = slugify(self.title)
        super(Product, self).save()

    def get_absolute_url(self):
        return reverse('blog:details', kwargs={'pk': self.id, 'slug': self.slug})

    def showImage(self):
        if self.active_image:
            return format_html(f'<img src="{self.active_image.url}" alt="" width="50px" height="50px">')
        else:
            return format_html('no image')

    showImage.short_description = 'product image'


class InformationProduct(models.Model):
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name='informations', blank=True, null=True)
    text = RichTextField()

    def __str__(self):
        return self.text[:15]


class Comment(models.Model):
    text = models.TextField()
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='comments')
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name='comments')
    parent = models.ForeignKey(
        'self', on_delete=models.CASCADE, null=True, blank=True, related_name='replies')
    status = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user} - {self.text[:40]}'

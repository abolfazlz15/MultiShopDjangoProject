import os
import uuid

from ckeditor.fields import RichTextField
from django.db import models
from django.urls import reverse
from django.utils.text import slugify


def get_file_path(instance, filename):
    ext = filename.split('.')[-1]
    filename = '%s.%s' % (uuid.uuid4(), ext)
    return os.path.join('product', filename)


class Category(models.Model):
    title = models.CharField(max_length=200)
    parent = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='parents')
    slug = models.SlugField(null=True, blank=True)

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        self.slug = slugify(self.title)
        super(Category, self).save()

    def __str__(self):
        return self.title


class ProductImage(models.Model):
    image = models.ImageField(blank=True, null=True, upload_to=get_file_path)

    # def __str__(self):
    #     return self.image

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
    active_image = models.ImageField(blank=True, null=True, upload_to=get_file_path)
    image = models.ManyToManyField(ProductImage, verbose_name='images', blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.BooleanField(default=False)
    category = models.ManyToManyField(Category, related_name='videos')
    size = models.ManyToManyField(ProductSize, related_name='product_size', blank=True)
    color = models.ManyToManyField(ProductColor, related_name='product_color', blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        self.slug = slugify(self.title)
        super(Product, self).save()

    # def get_absolute_url(self):
    #     return reverse('blog:details', kwargs={'slug': self.slug})

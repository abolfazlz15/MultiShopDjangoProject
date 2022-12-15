import os
import uuid

from ckeditor.fields import RichTextField
from django.db import models
from django.utils.text import slugify
from django.urls import reverse


def get_file_path(instance, filename):
    ext = filename.split('.')[-1]
    filename = '%s.%s' % (uuid.uuid4(), ext)
    return os.path.join('product', filename)


class Category(models.Model):
    title = models.CharField(max_length=200)
    parent = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='parents')
    slug = models.SlugField(max_length=200, unique=True)
    class Meta:
        ordering = ['title']

    verbose_name = 'category'
    verbose_name_plural = 'categories'

    def __str__(self):
        return self.name


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
    slug = models.SlugField()
    description = RichTextField()
    image = models.ForeignKey(ProductImage, verbose_name='image', on_delete=models.CASCADE, blank=True, null=True,)
    status = models.BooleanField(default=False)
    category = models.ManyToManyField(Category, related_name='videos')
    size = models.ManyToManyField(ProductSize, related_name='product_size', blank=True)
    color = models.ManyToManyField(ProductColor, related_name='product_color', blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.tilte

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        self.slug = slugify(self.title)
        super(Product, self).save()

    # def get_absolute_url(self):
    #     return reverse('blog:details', kwargs={'slug': self.slug})
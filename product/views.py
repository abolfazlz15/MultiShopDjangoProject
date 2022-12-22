from django.shortcuts import render
from django.views import generic
from product.models import Product


class ProductDetailView(generic.DetailView):
    template_name = 'product/product_detail.html'
    model = Product
    query_pk_and_slug = True
    context_object_name = 'product'



from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from order.cart import Cart
from product.models import Product
from order.forms import CartAddForm


class CartDetailView(View):
    def get(self, request):
        cart = Cart(request)

        return render(request, 'order/cart_detail.html', {'cart': cart})


class CartAddView(View):
    def post(self, request, product_id):
        cart = Cart(request)
        product = get_object_or_404(Product, id=product_id)
        form = CartAddForm(request.POST)
        if form.is_valid():
            clean_data = form.cleaned_data
            cart.add(product=product, quantity=clean_data['quantity'])
            return redirect('product:product_detail', product.id, product.slug)
        return redirect('product:product_detail', product.id, product.slug)


class CartDeleteView(View):
    def post(self, request, product_id):
        cart = Cart(request)
        product = get_object_or_404(Product, id=product_id)
        cart.remove(product)
        return redirect('order:cart-detail')

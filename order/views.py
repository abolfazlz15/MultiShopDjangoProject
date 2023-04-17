from decimal import Decimal

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect, render
from django.views import View

from order.cart import Cart
from order.models import DiscountCode, Order, OrderItem
from product.models import Product


class CartDetailView(View):
    def get(self, request):
        cart = Cart(request)

        return render(request, 'order/cart_detail.html', {'cart': cart})


class CartAddView(View):
    def post(self, request, product_id):
        cart = Cart(request)
        product = get_object_or_404(Product, id=product_id)
        quantity, color, size = request.POST.get('quantity'), request.POST.get('color'), request.POST.get('size')
        print(quantity, color, size)
        cart.add(product, quantity, size, color)
        return redirect('product:product-detail', product.id, product.slug)


class CartDeleteView(View):
    def post(self, request, id):
        cart = Cart(request)
        cart.remove(id)
        return redirect('order:cart-detail')


class OrderDetaiView(LoginRequiredMixin, View):
    def get(self, request, pk):
        order = get_object_or_404(Order, id=pk)
        return render(request, 'order/order_detail.html', context={'order': order})


class OrderCreationView(LoginRequiredMixin, View):
    def get(self, request):
        cart = Cart(request)
        order = Order.objects.create(user=request.user, total_price=cart.total())
        for item in cart:
            OrderItem.objects.create(order=order, product=item['product'], color=item['color'], size=item['size'],
                                     quantity=item['quantity'], price=item['price'])

        return redirect('order:order-detail', order.id)


class SubmitDiscountCodeView(LoginRequiredMixin, View):
    def post(self, request, pk):
        code = request.POST.get('discount_code')
        order = get_object_or_404(Order, id=pk)
        discount_code = DiscountCode.get(code, request.user)
        print(discount_code)
        if discount_code is None:
            messages.error(
                request,
                "This coupon does not exists!",
                'danger',
            )
            return redirect('order:order-detail', order.id)

        order.total_price -= order.total_price * discount_code.discount_percent/100
        order.save()
        return redirect('order:order-detail', order.id)

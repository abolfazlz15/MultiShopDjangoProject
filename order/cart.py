from django.conf import settings
from product.models import Product
from decimal import Decimal


class Cart(object):
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart

    def __iter__(self):
        product_ids = self.cart.keys()
        products = Product.objects.filter(id__in=product_ids)
        cart = self.cart.copy()
        for product in products:
            cart[str(product.id)]['product'] = product

        for i in cart.values():
            i['total_price'] = Decimal(i['price']) * i['quantity']
            i['total_price'] = i['price'] * i['quantity']
            yield i

    def __len__(self):
        return sum(i['quantity'] for i in self.cart.values())

    def get_total_price(self):
        return sum(Decimal(i['price'] * i['quantity'] for i in self.cart.values()))

    def clear(self):
        del self.session[settings.CART_SESSION_ID]
        self.save()

    def add(self, product, quantity):
        product_id = str(product.id)
        if product_id not in self.cart:
            self.cart[product_id] = {'quantity': 0, 'price': str(product.price)}
        self.cart[product_id]['quantity'] += quantity
        self.save()

    def save(self):
        self.session.modified = True

    def remove(self, product):
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

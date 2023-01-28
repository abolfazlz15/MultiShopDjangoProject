from decimal import Decimal

from product.models import Product


CART_SESSION_ID = 'cart'


class Cart(object):
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get(CART_SESSION_ID)
        if not cart:
            cart = self.session[CART_SESSION_ID] = {}
        self.cart = cart

    def __iter__(self):
        cart = self.cart.copy()


        for item in cart.values():
            item['product'] = Product.objects.get(id=int(item['id']))
            item['total_price'] = Decimal(item['price']) * item['quantity']
            item['unique_id'] = self.unique_id_generator(item['product'].id, item['color'], item['size'])
            yield item

   

    def clear(self):
        del self.session[CART_SESSION_ID]
        self.save()

    def unique_id_generator(self, id, color, size):
        result = f'{id}-{color}-{size}'
        return result

    def add(self, product, quantity, size, color):
        unique = self.unique_id_generator(product.id, color, size)

        if unique not in self.cart:
            self.cart[unique] = {'quantity': 0, 'price': str(product.price), 'color': color, 'size': size, 'id': str(product.id)}

        self.cart[unique]['quantity'] += int(quantity)
        self.save()

    def save(self):
        self.session.modified = True

    def remove(self, id):
        if id in self.cart:
            del self.cart[id]
            self.save()

    def total(self):
        cart = self.cart.values()
        total = 0
        for item in cart:
            total +=  Decimal(item['price']) * item['quantity']
        return total     
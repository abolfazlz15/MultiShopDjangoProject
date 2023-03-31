from product.models import Category
from order.cart import Cart

def categories(request):
    category = Category.objects.filter(parent=None)
    return {'categories': category}


def cart_total(request):
    cart = Cart(request)
    cart_total = sum(item['quantity'] for item in cart)
    return {'cart_total': cart_total}
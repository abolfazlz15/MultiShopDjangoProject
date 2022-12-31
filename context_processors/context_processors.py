from product.models import Category


def categories(request):
    category = Category.objects.filter(parent=None)
    return {'categories': category}
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect
from django.views import generic

from product.models import Category, Comment, Product


class ProductDetailView(generic.DetailView):
    template_name = 'product/product_detail.html'
    model = Product
    query_pk_and_slug = True
    context_object_name = 'product'


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product = self.get_object()
        category = product.category.first()
        related_products = Product.objects.filter(category=category).exclude(id=product.id)
        context['comments'] = Comment.objects.filter(status=True).filter(
            parent=None).filter(product=product).prefetch_related('user')
        context['related_products'] = related_products
        return context

    def post(self, request, pk, slug):
        text = request.POST.get('message')
        product = self.get_object()
        parent_id = request.POST.get('parent_id')
        user = request.user
        Comment.objects.create(text=text, product=product,
                               parent_id=parent_id, user=user)
        return redirect('product:product-detail', self.get_object().id, self.get_object().slug)


class ProductListView(generic.ListView):
    template_name = 'product/product_list.html'
    model = Product
    context_object_name = 'products'
    paginate_by = 3

    def get_queryset(self, *args, **kwargs):
        objects = super(ProductListView, self).get_queryset(*args, **kwargs)
        objects = objects.order_by("-id")
        return objects

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        request = self.request  
        colors = request.GET.getlist('color')
        sizes = request.GET.getlist('size')
        min_price = request.GET.get('min_price')
        max_price = request.GET.get('max_price')
        queryset = Product.objects.filter(status=True)

        if colors or sizes:
            queryset = queryset.filter(Q(color__tilte__in=colors) |
                                            Q(size__tilte__in=sizes) ).distinct()

        if min_price:
            queryset = queryset.filter(price__gte=min_price)

        if max_price:
            queryset = queryset.filter(price__lte=max_price)
   
        context['products'] = queryset
        return context


class SearchProductView(generic.ListView):
    model = Product
    template_name = 'product/product_list.html'
    context_object_name = 'products'

    def get_queryset(self):
        products = super().get_queryset()

        q = self.request.GET.get('search')
        if q:
            return Product.objects.filter(
                Q(title__icontains=q) |
                Q(category__title__icontains=q) |
                Q(description__icontains=q)
            ).filter(status=True).distinct()
        return products


class CategoryList(generic.ListView):
    template_name = 'product/all-product.html'
    context_object_name = 'products'

    def get_queryset(self):
        slug = self.kwargs['slug']
        category = get_object_or_404(Category, slug=slug)
        return category.products.all()
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from django.views import generic
from product.models import Category, Comment, Product


class ProductDetailView(generic.DetailView):
    template_name = 'product/product_detail.html'
    model = Product
    query_pk_and_slug = True
    context_object_name = 'product'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comments'] = Comment.objects.filter(status=True).filter(
            parent=None).filter(product=self.get_object())
        return context

    def post(self, request, pk, slug):
        text = request.POST.get('message')
        product = self.get_object()
        parent_id = request.POST.get('parent_id')
        user = request.user
        Comment.objects.create(text=text, product=product,
                               parent_id=parent_id, user=user)
        return redirect('product:product_detail', self.get_object().id, self.get_object().slug)


class ProductListView(generic.ListView):
    template_name = 'product/product_list.html'
    model = Product
    context_object_name = 'products'

    def get_queryset(self, *args, **kwargs):
        objects = super(ProductListView, self).get_queryset(*args, **kwargs)
        objects = objects.order_by("-id")
        return objects


class SearchProductView(generic.ListView):
    model = Product
    template_name = 'product/product_list.html'
    context_object_name = 'products'

    def get_queryset(self):
        products = super().get_queryset()

        q = self.request.GET.get('search')
        print(Product.objects.filter(
            Q(title__icontains=q) |
            Q(description__icontains=q)
        ).filter(status=True))
        if q:
            return Product.objects.filter(
                Q(title__icontains=q) |
                Q(category__title__icontains=q) |
                Q(description__icontains=q)
            ).filter(status=True)
        return products


class CategoryList(generic.ListView):
    template_name = 'videos/all-videos.html'
    context_object_name = 'products'

    def get_queryset(self):
        slug = self.kwargs['slug']
        category = get_object_or_404(Category, slug=slug)
        return category.products.all()

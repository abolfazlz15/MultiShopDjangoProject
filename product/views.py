from django.shortcuts import redirect, render
from django.views import generic

from product.models import Comment, Product


class ProductDetailView(generic.DetailView):
    template_name = 'product/product_detail.html'
    model = Product
    query_pk_and_slug = True
    context_object_name = 'product'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comments'] = Comment.objects.filter(
            status=True).filter(parent=None)
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

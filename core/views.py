from django.shortcuts import render
from django.urls import reverse
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin

from core.forms import ContactUsForm
from core.models import ContactUs
from product.models import Product, Category, FavoriteProduct
# from core.models import BannerHomePage

class ContactUsView(LoginRequiredMixin, generic.FormView):
    template_name = 'core/contact_us.html'
    form_class = ContactUsForm

    def get_success_url(self):
        return reverse('product:product-list')

    def form_valid(self, form):
        clean_data = form.cleaned_data
        ContactUs.objects.create(
            name=clean_data['name'], phone=self.request.user.phone, message=clean_data['message'])
        return super().form_valid(form)


class HomePageView(generic.TemplateView):
    template_name = 'core/home.html'

    def get_context_data(self, **kwargs):
        context = super(HomePageView, self).get_context_data(**kwargs)
        products = Product.objects.filter(status=True).order_by('-id')
        context['products'] = products[:4]
        context['products_old'] = products.order_by('created')
        context['categories'] = Category.objects.filter(parent=None).order_by('-id')
        # context['banners'] = BannerHomePage.objects.all()[:4]
        return context



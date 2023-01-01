from django.shortcuts import render
from django.views import generic
from core.forms import ContactUsForm
from core.models import ContactUs
from django.urls import reverse

class ContactUsView(generic.FormView):
    template_name = 'core/contact_us.html'
    form_class = ContactUsForm

    def get_success_url(self):
        return reverse('product:product_list')    

    def form_valid(self, form):
        clean_data = form.cleaned_data
        ContactUs.objects.create(
            name=clean_data['name'], email=self.request.user, message=clean_data['message'])
        return super().form_valid(form)
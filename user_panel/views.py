from django.shortcuts import render
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin

from order.models import Order


class IndexPageView(LoginRequiredMixin ,generic.TemplateView):
    template_name = 'user_panel/index.html'

    def get_context_data(self, **kwargs):
        context = super(IndexPageView, self).get_context_data(**kwargs)
        # order status in main page
        all_order = Order.objects.filter(user=self.request.user).values_list('status', flat=True)
        context['delivered_order'] = all_order.filter(status='Delivered').count()
        context['in_Progrssing_order'] = all_order.filter(status='In Progrssing').count()
        context['returned_order'] = all_order.filter(status='Returned').count()
        return context
    
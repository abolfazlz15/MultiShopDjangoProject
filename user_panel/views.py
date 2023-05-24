from django.shortcuts import render
from django.views import generic
from order.models import Order

class IndexPageView(generic.TemplateView):
    template_name = 'user_panel/index.html'

    def get_context_data(self, **kwargs):
        context = super(IndexPageView, self).get_context_data(**kwargs)
        all_order = Order.objects.values_list('status', flat=True)
        context['delivered_order'] = all_order.filter(status='Delivered').count()
        context['in_Progrssing_order'] = all_order.filter(status='In Progrssing').count()
        context['returned_order'] = all_order.filter(status='Returned').count()
        return context
    
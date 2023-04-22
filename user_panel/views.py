from django.shortcuts import render
from django.views import generic


class IndexPageView(generic.TemplateView):
    template_name = 'user_panel/index.html'

    def get_context_data(self, **kwargs):
        context = super(IndexPageView, self).get_context_data(**kwargs)
        return context
    
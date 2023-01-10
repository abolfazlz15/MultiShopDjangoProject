from django.shortcuts import render
from django.views import View


class CartDetailView(View):
    def get(self, request):
        return render(request, 'order/cart_detail.html')

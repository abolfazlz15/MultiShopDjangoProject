from django.urls import path
from order import views


app_name = 'order'
urlpatterns = [
    path('cart/detail', views.CartDetailView.as_view(), name='cart_detail')
]

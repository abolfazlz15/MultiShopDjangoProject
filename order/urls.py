from django.urls import path
from order import views

app_name = 'order'
urlpatterns = [
    path('cart/detail', views.CartDetailView.as_view(), name='cart-detail'),
    path('cart/add/<int:product_id>/', views.CartAddView.as_view(), name='cart-add'),
    path('cart/delete/<int:product_id>/', views.CartDeleteView .as_view(), name='cart-delete'),
]

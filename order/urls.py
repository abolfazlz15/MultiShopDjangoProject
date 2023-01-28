from django.urls import path
from order import views

app_name = 'order'
urlpatterns = [
    path('cart/detail', views.CartDetailView.as_view(), name='cart-detail'),
    path('cart/add/<int:product_id>/', views.CartAddView.as_view(), name='cart-add'),
    path('cart/delete/<str:id>/', views.CartDeleteView .as_view(), name='cart-delete'),

    # order URL
    path('detail/<int:pk>', views.OrderDetaiView.as_view(), name='order-detail'),
    path('add', views.OrderCreationView.as_view(), name='order-add'),
]

from django.urls import path
from product import views


app_name = 'product'
urlpatterns = [
    path('detail/<int:pk>/<slug:slug>', views.ProductDetailView.as_view(), name='product_detail'),
]
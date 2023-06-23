from django.urls import path
from product import views


app_name = 'product'
urlpatterns = [
    path('detail/<int:pk>/<slug:slug>', views.ProductDetailView.as_view(), name='product-detail'),
    path('', views.ProductListView.as_view(), name='product-list'),
    path('search/', views.SearchProductView.as_view(), name='product-search'),
    path('category/<slug:slug>', views.CategoryList.as_view(), name='category-product'),



]
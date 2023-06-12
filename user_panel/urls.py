from django.urls import path
from user_panel import views


app_name = 'user_panel'
urlpatterns = [
    path('', views.IndexPageView.as_view(), name='index'),
    path('profile', views.UserProfileView.as_view(), name='user_profile'),
    path('confirmphonenumber', views.ConfirmNewPhoneView.as_view(), name='confirm_phone'),
    path('order', views.OrderListView.as_view(), name='order_list'),
]

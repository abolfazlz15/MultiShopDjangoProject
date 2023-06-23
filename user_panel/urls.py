from django.urls import path
from user_panel import views


app_name = 'user_panel'
urlpatterns = [
    path('', views.IndexPageView.as_view(), name='index'),
    path('profile', views.UserProfileView.as_view(), name='user_profile'),
    path('order', views.OrderListView.as_view(), name='order_list'),
    path('favorite', views.FavoriteProductList.as_view(), name='favorite_product_list'),

    # Edit profile
    path('confirmphonenumber', views.ConfirmNewPhoneView.as_view(), name='confirm_phone'),
    path('confirmemail', views.ConfirmNewEmailView.as_view(), name='confirm_email'),
]

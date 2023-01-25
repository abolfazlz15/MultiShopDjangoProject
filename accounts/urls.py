from django.urls import path
from accounts import views


app_name = 'accounts'
urlpatterns = [
    path('login/', views.UserLoginView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('register/', views.UserRegisterView.as_view(), name='register'),
    path('check-otp/', views.CheckOTPView.as_view(), name='check-otp'),

    # add address URL
    path('addAddress', views.AddAddressView.as_view(), name='add-address'),
]
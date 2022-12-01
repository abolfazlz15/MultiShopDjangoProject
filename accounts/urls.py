from django.urls import path
from accounts import views


app_name = 'accounts'
urlpatterns = [
    path('login/', views.UserLoginView.as_view(), name='login'),
    path('register/', views.UserRegisterView.as_view(), name='register'),
    path('check-otp/', views.CheckOTPView.as_view(), name='check-otp'),
]
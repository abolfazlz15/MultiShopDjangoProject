from django.urls import path
from core import views


app_name = 'core'
urlpatterns = [
    path('', views.HomePageView.as_view(), name='home'),
    path('contactus', views.ContactUsView.as_view(), name='contact_us'),
]

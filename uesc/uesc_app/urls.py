from django.urls import path
from uesc_app import views

urlpatterns = [
    path('',views.home,name='home'),
]
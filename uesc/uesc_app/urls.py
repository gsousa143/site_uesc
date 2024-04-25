from django.urls import path
from uesc_app import views

urlpatterns = [
    path('',views.home,name='home'),
    path("noticias/",views.noticias,name="noticias"),
    path("editais/",views.editais,name="editais"),
    path("additens/",views.additens,name="additens")
]
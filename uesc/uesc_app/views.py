from django.shortcuts import render
from uesc_app.models import *

def home(request):
    link = Link.objects.order_by('id')
    contexto = {'link':link}
    return render(request,"index.html", contexto)

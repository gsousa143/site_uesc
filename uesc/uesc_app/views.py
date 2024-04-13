from django.shortcuts import render
from uesc_app.models import *

def home(request):
    tipos = Tipo.objects.all()
    grupos_por_tipo = {}
    
    for tipo in tipos:
        grupos_por_tipo[tipo] = Grupo.objects.filter(
            tipo=tipo).prefetch_related('link_set').all()
    
    contexto = {'grupos_por_tipo': grupos_por_tipo}
    return render(request, "index.html", contexto)

def noticias(request):
    noticias = Tipo.objects.all().filter(
        tipo="noticias").prefetch_related('link_set').all()
    contexto = {'noticias': noticias}
    return render(request, "noticias.html", contexto)

def editais(request):
    editais = Tipo.objects.all().filter(
        tipo="editais").prefetch_related('link_set').all()
    contexto = {'editais': editais}
    return render(request, "editais.html", contexto)



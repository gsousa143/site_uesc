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
    tipo_noticias = Tipo.objects.get(tipo="noticias")
    noticias = Grupo.objects.filter(tipo=tipo_noticias).prefetch_related('link_set').all()

    noticias_por_ano = {}
    for noticia in noticias:
        ano = noticia.data.year
        mes = noticia.data.strftime("%B")
        if ano not in noticias_por_ano:
            noticias_por_ano[ano] = {}
        if mes not in noticias_por_ano[ano]:
            noticias_por_ano[ano][mes] = []
        noticias_por_ano[ano][mes].append(noticia)

    contexto = {'noticias_por_ano': noticias_por_ano}
    return render(request, "noticias.html", contexto)

def editais(request):
    tipoEditais = Tipo.objects.get(
        tipo="editais")
    editais = Grupo.objects.filter(tipo=tipoEditais).prefetch_related('link_set').all()
    contexto = {'editais': editais}
    return render(request, "editais.html", contexto)


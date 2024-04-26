from django.shortcuts import render
from .models import *
from .forms import *
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import login as auth_login, logout as auth_logout, authenticate

def home(request):
    tipos = Tipo.objects.all()
    grupos_por_tipo = {}
    
    for tipo in tipos:
        grupos_por_tipo[tipo] = Grupo.objects.filter(
            tipo=tipo).prefetch_related('link_set').all()
        ''' Dicionario onde indice é referente ao tipo de grupo'''
    
    contexto = {'grupos_por_tipo': grupos_por_tipo}
    return render(request, "index.html", contexto)

def noticias(request):
    tipoNoticias = Tipo.objects.get(tipo="NOTICIAS")
    noticias = Grupo.objects.filter(tipo=tipoNoticias).prefetch_related('link_set').all()

    contexto = {'noticias': noticias}
    return render(request, "noticias.html", contexto)

def editais(request):
    tipoEditais = Tipo.objects.get(tipo="EDITAIS")
    editais = Grupo.objects.filter(tipo=tipoEditais).prefetch_related('link_set').all()
    contexto = {'editais': editais}
    return render(request, "editais.html", contexto)



def additens(request):
    form_link = LinkForm()
    form_grupo = GrupoForm()
    form_tipo = TipoForm()

    if request.method == 'POST':
        if 'submit_link' in request.POST:
            form_link = LinkForm(request.POST)
            if form_link.is_valid():
                form_link.save()
                return HttpResponseRedirect(reverse("home"))

        elif 'submit_grupo' in request.POST:
            form_grupo = GrupoForm(request.POST)
            if form_grupo.is_valid():
                form_grupo.save()
                return HttpResponseRedirect(reverse("home"))

        elif 'submit_tipo' in request.POST:
            form_tipo = TipoForm(request.POST)
            if form_tipo.is_valid():
                form_tipo.save()
                return HttpResponseRedirect(reverse("home"))
    
    contexto = {'form_link': form_link, 'form_grupo': form_grupo, 'form_tipo': form_tipo}
    return render(request, 'additens.html', contexto)



def login(request):
    form_login = LoginForm()
    contexto = {"form_login": form_login}
    if request.method=="POST":
        user = authenticate(username=request.POST.get("username"),password=request.POST.get("password"))
        if user:
            auth_login(request,user)
            return HttpResponseRedirect(reverse("additens"))

    return render(request,"login.html",contexto)


def logout(request):
    auth_logout(request)
    return HttpResponseRedirect("home")


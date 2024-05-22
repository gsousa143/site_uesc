from django.shortcuts import render, redirect
from .models import *
from .forms import *
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import login as auth_login, logout as auth_logout, authenticate
from django.contrib.auth.hashers import make_password
from django.contrib import messages
from django.contrib.auth.models import Permission

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
    tipo_noticias = Tipo.objects.get(tipo="NOTICIAS")
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
    tipo_editais = Tipo.objects.get(tipo="EDITAIS")
    editais = Grupo.objects.filter(tipo=tipo_editais).prefetch_related('link_set').all()

    editais_por_ano = {}
    for edital in editais:
        ano = edital.data.year
        mes = edital.data.strftime("%B")
        if ano not in editais_por_ano:
            editais_por_ano[ano] = {}
        if mes not in editais_por_ano[ano]:
            editais_por_ano[ano][mes] = []
        editais_por_ano[ano][mes].append(edital)

    contexto = {'editais_por_ano': editais_por_ano}
    return render(request, "editais.html", contexto)


def additens(request):
    form_link = LinkForm()
    form_grupo = GrupoForm()
    form_tipo = TipoForm()

    contexto = {"form_link": form_link, "form_grupo": form_grupo, "form_tipo": form_tipo}
    return render(request, "additens.html", contexto)

def formLink(request):
    form = LinkForm(request.POST)
    if form.is_valid():
        form.save()
    else:
        messages.error(request, 'Valor inválidos.')
    return HttpResponseRedirect(reverse("additens"))

def formGrupo(request):
    form = GrupoForm(request.POST)
    if form.is_valid():
        form.save()
    else:
        messages.error(request, 'Valor inválidos.')
    return HttpResponseRedirect(reverse("additens"))
    
def formTipo(request):
    form = TipoForm(request.POST)
    if form.is_valid():
        form.save()
    else:
        messages.error(request, 'Valor inválidos.')
    return HttpResponseRedirect(reverse("additens"))


def login(request):
    if request.method == "POST":
        user = authenticate(username=request.POST.get("username"),password=request.POST.get("password"))
        if user:
            auth_login(request,user = user)
        else:
            messages.error(request, 'Usuário ou senha inválidos.')
    return HttpResponseRedirect(reverse("usuario"))


def logout(request):
    auth_logout(request)
    return HttpResponseRedirect(reverse("usuario"))


def usuario(request):
    form_login = LoginForm()
    form_cadastro = cadastroForm()
    contexto = {"form_login": form_login,"form_cadastro":form_cadastro}

    return render(request,"usuario.html",contexto)


def cadastro(request):
    if request.method=="POST":
        form_cadastro = cadastroForm(request.POST)
        if form_cadastro.is_valid():
            if request.POST.get("password")!=request.POST.get("confirmacao"):
                form_cadastro.add_error("password","As senhas devem ser iguais")
            else:
                form_cadastro = form_cadastro.save(commit=False)
                form_cadastro.password = make_password(form_cadastro.password)
                form_cadastro.save()
                return HttpResponseRedirect(reverse("home"))

    form_cadastro = cadastroForm()
    contexto = {"form_cadastro":form_cadastro}
    return render(request,"cadastro.html",contexto)


def remover(request,id):
        user = User.objects.get(id=id)
        user.delete()
        auth_logout(request)
        return HttpResponseRedirect(reverse("home"))




def editarUsuario (request,id):
    if request.method == 'POST':
        usuario = User.objects.get(id=id)
        novo_usuario = request.POST.copy()
        user = cadastroForm(instance=usuario, data=novo_usuario)
        if user.is_valid:
            user.save()
    return HttpResponseRedirect(reverse('home'))


def adm(request):
    if request.method == "GET" and request.user.is_superuser:
        usuarios = User.objects.all;
        contexto = {"usuarios":usuarios}
        return render(request, "adm.html", contexto)
    return HttpResponseRedirect(reverse('home'))


def editarpermissao(request,id):
    usuario = User.objects.get(id = id)
    form_cadastro = cadastroForm()
    contexto = {"usuario":usuario,"form_cadastro":form_cadastro}
    return render(request, "editarpermissao.html", contexto)


def alternaractive(request,id):
    usuario = User.objects.get(id = id)
    usuario.is_active = not usuario.is_active
    usuario.save()
    return HttpResponseRedirect(reverse("adm"))



def alternarsuperuser(request,id):
    usuario = User.objects.get(id = id)
    usuario.is_superuser = not usuario.is_superuser
    usuario.save()
    return HttpResponseRedirect(reverse("adm"))


def alternarstaff(request,id):
    usuario = User.objects.get(id = id)
    usuario.is_staff = not usuario.is_staff
    usuario.save()
    return HttpResponseRedirect(reverse("adm"))


def admusuario(request,id):
    usuario = User.objects.get(id=id)
    permissoes = Permission.objects.order_by("id")
    form_cadastro = cadastroForm()
    contexto = {
        "usuario":usuario,
        "permissoes":permissoes,
        "form_cadastro":form_cadastro}
    return render(request,"admusuario.html",contexto)
    
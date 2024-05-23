from django.shortcuts import render
from .models import *
from .forms import *
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import login as auth_login, logout as auth_logout, authenticate
from django.contrib.auth.hashers import make_password
from django.contrib import messages
from django.contrib.auth.models import Permission, Group

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


def add_itens(request):
    form_link = LinkForm()
    form_grupo = GrupoForm()
    form_tipo = TipoForm()

    contexto = {"form_link": form_link, "form_grupo": form_grupo, "form_tipo": form_tipo}
    return render(request, "add_itens.html", contexto)

def add_link(request):
    form = LinkForm(request.POST)
    if form.is_valid():
        form.save()
    else:
        messages.error(request, 'Valor inválidos.')
    return HttpResponseRedirect(reverse("additens"))

def add_grupo(request):
    form = GrupoForm(request.POST)
    if form.is_valid():
        form.save()
    else:
        messages.error(request, 'Valor inválidos.')
    return HttpResponseRedirect(reverse("additens"))
    
def add_tipo(request):
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
    return HttpResponseRedirect(reverse("perfil"))


def logout(request):
    auth_logout(request)
    return HttpResponseRedirect(reverse("home"))


def perfil(request):
    form_usuario = UsuarioForm()
    if request.user.is_authenticated:
        form_usuario = UsuarioForm(instance=request.user)
    contexto = {"form_usuario": form_usuario}

    return render(request,"perfil.html",contexto)


def cadastro(request):
    if request.method=="POST":
        form_usuario = UsuarioForm(request.POST)
        if form_usuario.is_valid():
            if request.POST.get("password")!=request.POST.get("confirmacao"):
                form_usuario.add_error("password","As senhas devem ser iguais")
            else:
                form_usuario = form_usuario.save(commit=False)
                form_usuario.password = make_password(form_usuario.password)
                form_usuario.save()
                return HttpResponseRedirect(reverse("home"))

    form_usuario = UsuarioForm()
    contexto = {"form_usuario":form_usuario}
    return render(request,"cadastro.html",contexto)


def remover(request,id):
    if request.user.is_authenticaded:
        user = User.objects.get(id=id)
        user.delete()
        auth_logout(request)
    return HttpResponseRedirect(reverse("home"))







def painel(request):
    if request.method == "GET" and request.user.is_authenticated and request.user.is_superuser:
        usuarios = User.objects.all;
        contexto = {"usuarios":usuarios}
        return render(request, "painel.html", contexto)
    return HttpResponseRedirect(reverse('home'))



def alternar_active(request,id):
    if request.user.is_authenticated and request.user.is_superuser:
        usuario = User.objects.get(id = id)
        usuario.is_active = not usuario.is_active
        usuario.save()
        return HttpResponseRedirect(reverse("painel"))
    else:
        return HttpResponseRedirect(reverse("home"))



def alternar_superuser(request,id):
    if request.user.is_authenticated and request.user.is_superuser:
        usuario = User.objects.get(id = id)
        usuario.is_superuser = not usuario.is_superuser
        usuario.save()
        return HttpResponseRedirect(reverse("painel"))
    else:
        return HttpResponseRedirect(reverse("home"))

def alternar_staff(request,id):
    if request.user.is_authenticated and request.user.is_superuser:
        usuario = User.objects.get(id = id)
        usuario.is_staff = not usuario.is_staff
        usuario.save()
        return HttpResponseRedirect(reverse("painel"))
    else:
        return HttpResponseRedirect(reverse("home"))


def editar_usuario(request, id):
    if request.user.is_authenticated and request.user.is_superuser:
        permissoes = Permission.objects.order_by('id')
        permissoes_agrupadas = {}
        for permissao in permissoes:
            objeto = permissao.codename.split("_")
            if objeto[1] not in permissoes_agrupadas:
                permissoes_agrupadas[objeto[1]] = {objeto[0]: permissao.id}
            else:
                permissoes_agrupadas[objeto[1]][objeto[0]] = permissao.id

        usuario = User.objects.get(id=id)
        form_usuario = UsuarioForm(instance=usuario)
        permissoes_usuario = usuario.user_permissions.values_list('id', flat=True)

        contexto = {
            "usuario": usuario,
            "permissoes": permissoes_agrupadas,
            "form_usuario": form_usuario,
            "grupos": Group.objects.all(),
            "permissoes_usuario": permissoes_usuario,
        }

        return render(request, "editar_usuario.html", contexto)
    else:
        return HttpResponseRedirect(reverse("home"))
    
    


def editar_usuario_painel(request, id):
    if request.method == 'POST' and request.user.is_authenticated and request.user.is_superuser:
        usuario = User.objects.get(id=id)
        novo_usuario = request.POST.copy()
        novo_usuario["password"] = usuario.password  # Keep the existing password
        user_form = UsuarioForm(instance=usuario, data=novo_usuario)

        if user_form.is_valid():
            user = user_form.save(commit=False)
            user.password = usuario.password  # Ensure password is not hashed again
            user.save()

            # Prepare the permission list
            permlist = []
            permissoes = request.POST.getlist("permissoes")
            for permissao in permissoes:
                permlist.append(Permission.objects.get(id=permissao))

            user.user_permissions.set(permlist)
            user.save()

            return HttpResponseRedirect(reverse('painel'))
        else:
            permissoes = Permission.objects.order_by('id')
            permissoes_agrupadas = {}
            for permissao in permissoes:
                objeto = permissao.codename.split("_")
                if objeto[1] not in permissoes_agrupadas:
                    permissoes_agrupadas[objeto[1]] = {objeto[0]: permissao.id}
                else:
                    permissoes_agrupadas[objeto[1]][objeto[0]] = permissao.id

            permissoes_usuario = usuario.user_permissions.values_list('id', flat=True)

            contexto = {
                "usuario": usuario,
                "permissoes": permissoes_agrupadas,
                "form_usuario": user_form,
                "grupos": Group.objects.all(),
                "permissoes_usuario": permissoes_usuario,
            }
            return render(request, "editar_usuario.html", contexto)

    return HttpResponseRedirect(reverse('home'))





def criar_usuario(request):
    if request.user.is_authenticated and request.user.is_superuser:
        form = UsuarioForm
        permissoes = Permission.objects.order_by('id')
        permissoes_agrupadas = {}
        for permissao in permissoes:
            objeto = permissao.codename.split("_")
            if objeto[1] not in permissoes_agrupadas:
                permissoes_agrupadas[objeto[1]] = {objeto[0]: permissao.id}
            else:
                permissoes_agrupadas[objeto[1]][objeto[0]] = permissao.id
        contexto = {
            "form_usuario": form,
            "permissoes": permissoes_agrupadas}

        return render(request,"criar_usuario.html", contexto)
    return HttpResponseRedirect(reverse("home"))
    
def criar_usuario_painel(request):
    if request.method=="POST" and request.user.is_authenticated and request.user.is_superuser:
        form_usuario = UsuarioForm(request.POST)
        if form_usuario.is_valid():
            
            permlist = []
            permissoes = request.POST.getlist("permissoes")
            for permissao in permissoes:
                permlist.append(Permission.objects.get(id=permissao))
            
            form_usuario = form_usuario.save(commit=False)
            form_usuario.password = make_password(form_usuario.password)
            form_usuario.save()
            form_usuario.user_permissions.set(permlist)
            form_usuario.save()
            return HttpResponseRedirect(reverse("painel"))
        
    return HttpResponseRedirect(reverse("home"))
        

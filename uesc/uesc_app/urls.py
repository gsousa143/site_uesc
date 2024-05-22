from django.urls import path
from uesc_app import views

urlpatterns = [
    path('',views.home,name='home'),
    path("noticias/",views.noticias,name="noticias"),
    path("editais/",views.editais,name="editais"),

    path("additens/",views.additens,name="additens"),
    path("addtipo/",views.formTipo,name="formTipo"),
    path("addgrupo/",views.formGrupo,name="formGrupo"),
    path("addlink/",views.formLink,name="formLink"),


    path("usuario/",views.usuario,name="usuario"),
    path("login/",views.login,name="login"),
    path("logout/",views.logout,name="logout"),
    path("cadastro/",views.cadastro,name="cadastro"),
    path("remover/<id>",views.remover, name="remover"),
    path("editarusuario/<id>",views.editarUsuario,name="editarusuario"),


    path("adm",views.adm,name="adm"),
    path("admusuario/<id>",views.admusuario,name="admusuario"),
    path("alternaractive/<id>",views.alternaractive,name="alternaractive"),
    path("alternarsuperuser/<id>",views.alternarsuperuser,name="alternarsuperuser"),
    path("alternarstaff/<id>",views.alternarstaff,name="alternarstaff"),
    

]
from django.urls import path
from uesc_app import views

urlpatterns = [
    path('',views.home,name='home'),
    path("noticias/",views.noticias,name="noticias"),
    path("editais/",views.editais,name="editais"),

    path("add_itens/",views.add_itens,name="add_itens"),
    path("add_tipo/",views.add_tipo,name="add_tipo"),
    path("add_grupo/",views.add_grupo,name="add_grupo"),
    path("add_link/",views.add_link,name="add_link"),


    path("perfil/",views.perfil,name="perfil"),
    path("login/",views.login,name="login"),
    path("logout/",views.logout,name="logout"),
    path("cadastro/",views.cadastro,name="cadastro"),
    path("editar_usuario_perfil/",views.editar_usuario_perfil,name="editar_usuario_perfil"),
    path("remover_usuario/<id>",views.remover_usuario, name="remover_usuario"),

    

    path("painel",views.painel,name="painel"),

    path("criar_usuario/",views.criar_usuario,name="criar_usuario"),
    path("criar_usuario_painel/",views.criar_usuario_painel,name="criar_usuario_painel"),

    path("editar_usuario/<id>",views.editar_usuario,name="editar_usuario"),
    path("editar_usuario_painel/<id>",views.editar_usuario_painel,name="editar_usuario_painel"),

    path("alternar_active/<id>",views.alternar_active,name="alternar_active"),
    path("alternar_superuser/<id>",views.alternar_superuser,name="alternar_superuser"),
    path("alternar_staff/<id>",views.alternar_staff,name="alternar_staff"),

    path('criar_grupo/', views.criar_grupo, name='criar_grupo'),
    path('criar_grupo_painel/', views.criar_grupo_painel, name='criar_grupo_painel'),
    path('editar_grupo/<id>',views.editar_grupo,name="editar_grupo"),
    path('editar_grupo_painel/<id>',views.editar_grupo_painel,name="editar_grupo_painel"),

    path('remover_grupo/<id>', views.remover_grupo, name="remover_grupo")
    
]
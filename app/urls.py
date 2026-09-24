from django.urls import path

from . import views

urlpatterns = [
    path("", views.login_view, name="login"),
    path("cadastro/", views.cadastro_view, name="cadastro"),
    path("boas-vindas/", views.boas_vindas_view, name="boas_vindas"),
    path("sair/", views.logout_view, name="logout"),
    path("materias/", views.materias_view, name="materias"),
    path("materias/<int:materia_id>/", views.conteudos_view, name="conteudos"),
    path("conteudo/<int:conteudo_id>/", views.leitura_view, name="leitura"),
    path("salvar-progresso/", views.salvar_progresso_view, name="salvar_progresso"),
    path("questoes/<int:conteudo_id>/", views.questoes_view, name="questoes"),
    path("responder/<int:conteudo_id>/", views.responder_view, name="responder"),
    path("resultado/<int:conteudo_id>/", views.resultado_view, name="resultado"),
    path("ranking/", views.ranking_view, name="ranking"),
    # Forum
    path("forum/", views.forum_view, name="forum"),
    path("forum/topic/<int:pk>/", views.topico_view, name="topico"),
    path("forum/criar-topico/", views.criar_topico_view, name="criar_topico"),
    path("forum/responder/<int:pk>/", views.responder_view, name="responder_forum"),
]
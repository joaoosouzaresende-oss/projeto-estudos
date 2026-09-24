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
]
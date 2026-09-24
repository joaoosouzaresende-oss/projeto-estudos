from datetime import timedelta
import json

from django.contrib.auth.models import User
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.views.decorators.http import require_POST

from .forms import CadastroForm, LoginForm
from .models import LoginAttempt, Perfil, Materia, Conteudo, ProgressoLeitura, Questao

MAX_TENTATIVAS = 3
BLOQUEIO_MINUTOS = 15


def _get_attempt(username):
    attempt, _ = LoginAttempt.objects.get_or_create(username=username)
    return attempt


def _bloqueado(attempt):
    if attempt.bloqueado_ate and timezone.now() < attempt.bloqueado_ate:
        return True
    if attempt.bloqueado_ate and timezone.now() >= attempt.bloqueado_ate:
        attempt.tentativas = 0
        attempt.bloqueado_ate = None
        attempt.save()
    return False


def login_view(request):
    if request.user.is_authenticated:
        return redirect("materias")

    form = LoginForm(request.POST or None)
    erro = None

    if request.method == "POST" and form.is_valid():
        nome = form.cleaned_data["nome"].strip()
        senha = form.cleaned_data["senha"]

        attempt = _get_attempt(nome)

        if _bloqueado(attempt):
            restante = attempt.bloqueado_ate - timezone.now()
            minutos = max(int(restante.total_seconds() // 60), 1)
            erro = f"Conta bloqueada por tentativas incorretas. Tente novamente em {minutos} min."
        else:
            try:
                usuario = User.objects.get(username__iexact=nome)
            except User.DoesNotExist:
                erro = "Conta nÃ£o encontrada. VocÃª ainda nÃ£o tem conta? Cadastre-se."
            else:
                if usuario.check_password(senha):
                    attempt.tentativas = 0
                    attempt.bloqueado_ate = None
                    attempt.save()
                    login(request, usuario)
                    return redirect("materias")
                else:
                    attempt.tentativas += 1
                    if attempt.tentativas >= MAX_TENTATIVAS:
                        attempt.bloqueado_ate = timezone.now() + timedelta(minutes=BLOQUEIO_MINUTOS)
                        erro = f"Senha incorreta. Conta bloqueada por {BLOQUEIO_MINUTOS} minutos apÃ³s {MAX_TENTATIVAS} tentativas."
                    else:
                        restantes = MAX_TENTATIVAS - attempt.tentativas
                        erro = f"Senha incorreta. {restantes} tentativa(s) restante(s)."
                    attempt.save()

    return render(request, "login.html", {"form": form, "erro": erro})


def cadastro_view(request):
    if request.user.is_authenticated:
        return redirect("materias")

    form = CadastroForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        nome = form.cleaned_data["nome"]
        usuario = User.objects.create_user(
            username=nome,
            email=form.cleaned_data["email"],
            password=form.cleaned_data["senha"],
        )
        Perfil.objects.create(
            usuario=usuario,
            telefone=form.cleaned_data.get("telefone", ""),
        )
        login(request, usuario)
        return redirect("materias")

    return render(request, "cadastro.html", {"form": form})


def boas_vindas_view(request):
    if not request.user.is_authenticated:
        return redirect("login")
    return render(request, "boas_vindas.html")


def logout_view(request):
    logout(request)
    return redirect("login")


@login_required(login_url="login")
def materias_view(request):
    materias = Materia.objects.all()
    return render(request, "materias.html", {"materias": materias})


@login_required(login_url="login")
def conteudos_view(request, materia_id):
    materia = get_object_or_404(Materia, id=materia_id)
    progressos = {
        p.conteudo_id: p.percentual
        for p in ProgressoLeitura.objects.filter(usuario=request.user, conteudo__materia=materia)
    }
    conteudos = [
        {"objeto": c, "percentual": progressos.get(c.id, 0)}
        for c in materia.conteudos.all()
    ]
    return render(request, "conteudos.html", {"materia": materia, "conteudos": conteudos})


@login_required(login_url="login")
def leitura_view(request, conteudo_id):
    conteudo = get_object_or_404(Conteudo, id=conteudo_id)
    progresso, _ = ProgressoLeitura.objects.get_or_create(
        usuario=request.user, conteudo=conteudo
    )
    return render(request, "leitura.html", {"conteudo": conteudo, "progresso": progresso})


@require_POST
@login_required(login_url="login")
def salvar_progresso_view(request):
    conteudo_id = request.POST.get("conteudo_id")
    percentual = request.POST.get("percentual", 0)

    if not conteudo_id:
        return JsonResponse({"ok": False, "erro": "conteudo_id ausente"}, status=400)

    try:
        percentual = int(percentual)
    except (TypeError, ValueError):
        return JsonResponse({"ok": False, "erro": "percentual invÃ¡lido"}, status=400)

    percentual = max(0, min(percentual, 100))
    ProgressoLeitura.objects.update_or_create(
        usuario=request.user,
        conteudo_id=int(conteudo_id),
        defaults={"percentual": percentual},
    )
    return JsonResponse({"ok": True, "percentual": percentual})


@login_required(login_url="login")
def questoes_view(request, conteudo_id):
    conteudo = get_object_or_404(Conteudo, id=conteudo_id)
    questoes = list(conteudo.questoes.all())

    if not questoes:
        return render(request, "questoes.html", {
            "conteudo": conteudo,
            "questoes": [],
            "mensagem": "Nenhuma questão disponível para este conteúdo ainda.",
        })

    request.session["quiz"] = {
        "conteudo_id": conteudo.id,
        "questao_index": 0,
        "total": len(questoes),
        "acertos": 0,
        "respostas": [],
    }

    return render(request, "questoes.html", {
        "conteudo": conteudo,
        "questoes": questoes,
        "questao_atual": questoes[0],
        "indice": 0,
    })


@login_required(login_url="login")
def responder_view(request, conteudo_id):
    if request.method != "POST":
        return redirect("questoes", conteudo_id=conteudo_id)

    quiz = request.session.get("quiz")
    if not quiz or quiz["conteudo_id"] != conteudo_id:
        return redirect("questoes", conteudo_id=conteudo_id)

    questoes = list(Conteudo.objects.get(id=conteudo_id).questoes.all())
    indice = quiz["questao_index"]

    if indice >= len(questoes):
        return redirect("resultado", conteudo_id=conteudo_id)

    questao = questoes[indice]
    alternativa = request.POST.get("alternativa", "")

    acertou = alternativa == questao.resposta
    if acertou:
        quiz["acertos"] += 1
        perfil, _ = Perfil.objects.get_or_create(usuario=request.user)
        perfil.pontuacao += 10
        perfil.save()

    quiz["respostas"].append({
        "questao_id": questao.id,
        "escolhida": alternativa,
        "correta": questao.resposta,
        "acertou": acertou,
    })
    quiz["questao_index"] = indice + 1
    request.session["quiz"] = quiz

    return render(request, "resposta.html", {
        "questao": questao,
        "escolhida": alternativa,
        "acertou": acertou,
        "indice": indice,
        "total": quiz["total"],
        "proxima_disponivel": indice + 1 < quiz["total"],
    })


@login_required(login_url="login")
def resultado_view(request, conteudo_id):
    quiz = request.session.get("quiz")
    if not quiz or quiz["conteudo_id"] != conteudo_id:
        return redirect("materias")

    conteudo = get_object_or_404(Conteudo, id=conteudo_id)
    total = quiz["total"]
    acertos = quiz["acertos"]
    desempenho = round((acertos / total) * 100) if total > 0 else 0

    del request.session["quiz"]

    return render(request, "resultado.html", {
        "conteudo": conteudo,
        "acertos": acertos,
        "total": total,
        "desempenho": desempenho,
    })


@login_required(login_url="login")
def ranking_view(request):
    perfis = Perfil.objects.select_related("usuario").order_by("-pontuacao")[:100]
    posicao_usuario = None
    for i, p in enumerate(perfis, start=1):
        if p.usuario == request.user:
            posicao_usuario = i
            break

    perfil, _ = Perfil.objects.get_or_create(usuario=request.user)

    if posicao_usuario is None:
        posicao_geral = Perfil.objects.filter(
            pontuacao__gt=perfil.pontuacao
        ).count() + 1
    else:
        posicao_geral = posicao_usuario

    return render(request, "ranking.html", {
        "perfis": perfis,
        "posicao_usuario": posicao_usuario,
    })


def _puede_responder(usuario, pergunta):
    """Verifica se o usuário pode responder (máx 3 respostas seguidas sem interação)."""
    from django.db.models import Q
    ultimas_respostas = Forum_Resposta.objects.filter(
        pergunta=pergunta
    ).order_by("-criado_em")
    contador = 0
    for r in ultimas_respostas:
        if r.usuario == usuario:
            contador += 1
            if contador >= 3:
                return False
        else:
            contador = 0
    return True


@login_required(login_url="login")
def forum_view(request):
    """Lista todos os tópicos de dúvida ordenados por data (mais recentes primeiro)."""
    topicos = Forum_Pergunta.objects.all().order_by("-criado_em")
    return render(request, "forum.html", {"topicos": topicos})


@login_required(login_url="login")
def topico_view(request, pk):
    """Visualiza um tópico específico e suas respostas cronologicamente."""
    pergunta = get_object_or_404(Forum_Pergunta, pk=pk)
    respostas = pergunta.respostas.all().order_by("criado_em")
    pode_responder = _puede_responder(request.user, pergunta)
    return render(request, "topico.html", {
        "pergunta": pergunta,
        "respostas": respostas,
        "pode_responder": pode_responder,
    })


@login_required(login_url="login")
def criar_topico_view(request):
    """Permite ao usuário criar um novo tópico de dúvida."""
    if request.method == "POST":
        titulo = request.POST.get("titulo")
        descricao = request.POST.get("descricao", "")
        Forum_Pergunta.objects.create(
            titulo=titulo,
            descricao=descricao,
            criado_por=request.user,
        )
        return redirect("forum")
    return render(request, "criar_topico.html")


@login_required(login_url="login")
def responder_view(request, pk):
    """Permite ao usuário responder um tópico (respectando a regra de 3 respostas seguidas)."""
    pergunta = get_object_or_404(Forum_Pergunta, pk=pk)
    if request.method == "POST":
        conteudo = request.POST.get("conteudo", "").strip()
        if conteudo and _puede_responder(request.user, pergunta):
            Forum_Resposta.objects.create(
                pergunta=pergunta,
                usuario=request.user,
                conteudo=conteudo,
            )
        return redirect("topico", pk=pk)
    return redirect("topico", pk=pk)

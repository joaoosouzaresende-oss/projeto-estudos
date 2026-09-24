from django.db import models
from django.contrib.auth.models import User


class Perfil(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE, related_name="perfil")
    telefone = models.CharField(max_length=15, blank=True)
    pontuacao = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"Perfil de {self.usuario.username}"


class LoginAttempt(models.Model):
    username = models.CharField(max_length=150, unique=True)
    tentativas = models.PositiveIntegerField(default=0)
    bloqueado_ate = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.username} — {self.tentativas} tentativas"


class Materia(models.Model):
    nome = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.nome

    class Meta:
        verbose_name = "Matéria"
        verbose_name_plural = "Matérias"
        ordering = ["nome"]


class Conteudo(models.Model):
    materia = models.ForeignKey(Materia, on_delete=models.CASCADE, related_name="conteudos")
    nome = models.CharField(max_length=200)
    conteudo = models.TextField()
    referencia = models.URLField(blank=True)

    def __str__(self):
        return f"{self.nome} ({self.materia.nome})"

    class Meta:
        verbose_name = "Conteúdo"
        verbose_name_plural = "Conteúdos"
        ordering = ["nome"]


class ProgressoLeitura(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name="progressos_leitura")
    conteudo = models.ForeignKey(Conteudo, on_delete=models.CASCADE, related_name="progressos")
    percentual = models.PositiveIntegerField(default=0)

    class Meta:
        verbose_name = "Progresso de leitura"
        verbose_name_plural = "Progressos de leitura"
        unique_together = ("usuario", "conteudo")

    def __str__(self):
        return f"{self.usuario.username} — {self.conteudo.nome} ({self.percentual}%)"


class Questao(models.Model):
    RESPOSTAS = [
        ("A", "A"),
        ("B", "B"),
        ("C", "C"),
        ("D", "D"),
        ("E", "E"),
    ]

    conteudo = models.ForeignKey(Conteudo, on_delete=models.CASCADE, related_name="questoes")
    enunciado = models.TextField()
    alt_a = models.TextField()
    alt_b = models.TextField()
    alt_c = models.TextField()
    alt_d = models.TextField()
    alt_e = models.TextField()
    resposta = models.CharField(max_length=1, choices=RESPOSTAS)
    comentario = models.TextField(blank=True)

    def __str__(self):
        return f"Questão #{self.pk} ({self.conteudo.materia.nome})"

    class Meta:
        verbose_name = "Questão"
        verbose_name_plural = "Questões"
        ordering = ["pk"]

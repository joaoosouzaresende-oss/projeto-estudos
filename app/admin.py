from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

from .models import Forum_Pergunta, Forum_Resposta, Perfil, LoginAttempt, Materia, Conteudo, ProgressoLeitura, Questao


class PerfilInline(admin.StackedInline):
    model = Perfil
    can_delete = False
    verbose_name_plural = "Perfil"
    fk_name = "usuario"


class UsuarioAdmin(UserAdmin):
    inlines = [PerfilInline]
    list_display = ("username", "email", "perfil_telefone", "is_staff")
    search_fields = ("username", "email")

    @admin.display(description="Telefone")
    def perfil_telefone(self, obj):
        perfil = obj.perfil if hasattr(obj, "perfil") else None
        return perfil.telefone if perfil else "—"


admin.site.unregister(User)
admin.site.register(User, UsuarioAdmin)


class PerfilAdmin(admin.ModelAdmin):
    list_display = ("usuario_username", "usuario_email", "telefone")
    search_fields = ("usuario__username", "usuario__email", "telefone")

    @admin.display(description="Nome")
    def usuario_username(self, obj):
        return obj.usuario.username

    @admin.display(description="Email")
    def usuario_email(self, obj):
        return obj.usuario.email


admin.site.register(Perfil, PerfilAdmin)
admin.site.register(LoginAttempt)


class ConteudoInline(admin.TabularInline):
    model = Conteudo
    extra = 1


class MateriaAdmin(admin.ModelAdmin):
    list_display = ("nome", "quantidade_conteudos")
    search_fields = ("nome",)
    inlines = [ConteudoInline]

    @admin.display(description="Conteúdos")
    def quantidade_conteudos(self, obj):
        return obj.conteudos.count()


class ConteudoAdmin(admin.ModelAdmin):
    list_display = ("nome", "materia", "referencia")
    list_filter = ("materia",)
    search_fields = ("nome", "materia__nome")


class ProgressoLeituraAdmin(admin.ModelAdmin):
    list_display = ("usuario", "conteudo", "percentual")
    list_filter = ("usuario",)


admin.site.register(Materia, MateriaAdmin)
admin.site.register(Conteudo, ConteudoAdmin)
admin.site.register(ProgressoLeitura, ProgressoLeituraAdmin)


class QuestaoAdmin(admin.ModelAdmin):
    list_display = ("pk", "materia_nome", "resposta", "conteudo")
    list_filter = ("conteudo__materia",)
    search_fields = ("enunciado", "conteudo__materia__nome")

    @admin.display(description="Matéria")
    def materia_nome(self, obj):
        return obj.conteudo.materia.nome


admin.site.register(Questao, QuestaoAdmin)


class Forum_PerguntaAdmin(admin.ModelAdmin):
    list_display = ("titulo", "criado_por", "criado_em")
    list_filter = ("criado_em",)
    search_fields = ("titulo", "descricao", "criado_por__username")


class Forum_RespostaAdmin(admin.ModelAdmin):
    list_display = ("pergunta_titulo", "usuario", "criado_em")
    list_filter = ("criado_em",)
    search_fields = ("conteudo", "usuario__username", "pergunta__titulo")

    @admin.display(description="Tópico")
    def pergunta_titulo(self, obj):
        return obj.pergunta.titulo


admin.site.register(Forum_Pergunta, Forum_PerguntaAdmin)
admin.site.register(Forum_Resposta, Forum_RespostaAdmin)
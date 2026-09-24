from django import forms
from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from .models import Perfil

telefone_validator = RegexValidator(
    regex=r"^\d{10,15}$",
    message="Telefone deve conter apenas números, entre 10 e 15 dígitos.",
)


class LoginForm(forms.Form):
    nome = forms.CharField(label="Nome", max_length=150, widget=forms.TextInput(attrs={"required": True}))
    senha = forms.CharField(label="Senha", widget=forms.PasswordInput(attrs={"required": True}))

class CadastroForm(forms.Form):
    nome = forms.CharField(label="Nome", max_length=150, widget=forms.TextInput(attrs={"required": True}))
    email = forms.EmailField(label="Email", widget=forms.EmailInput(attrs={"required": True}))
    telefone = forms.CharField(
        label="Telefone",
        max_length=15,
        widget=forms.TextInput(attrs={"required": True, "inputmode": "numeric", "pattern": r"\d{10,15}"}),
        validators=[telefone_validator],
    )
    senha = forms.CharField(label="Senha", widget=forms.PasswordInput(attrs={"required": True}))

    def clean_nome(self):
        nome = self.cleaned_data["nome"].strip()
        if User.objects.filter(username__iexact=nome).exists():
            raise forms.ValidationError("Já existe uma conta com esse nome. Faça login.")
        return nome
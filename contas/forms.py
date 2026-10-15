from django import forms
from django.contrib.auth.models import User
from allauth.account.forms import SignupForm
from .models import Perfil


class CustomSignupForm(SignupForm):
    first_name = forms.CharField(
        max_length=150,
        label='Nome completo',
        widget=forms.TextInput(attrs={'placeholder': 'Seu nome'})
    )

    def save(self, request):
        user = super().save(request)
        user.first_name = self.cleaned_data['first_name']
        user.save()
        return user


class EditarUsuarioForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'first_name']
        labels = {
            'username': 'Nome de usuário',
            'first_name': 'Nome completo',
        }


class EditarPerfilForm(forms.ModelForm):
    class Meta:
        model = Perfil
        fields = ['foto_perfil', 'descricao', 'publico']
        labels = {
            'foto_perfil': 'Foto de perfil',
            'descricao': 'Descrição',
            'publico': 'Perfil público',
        }
        widgets = {
            'descricao': forms.Textarea(attrs={'maxlength': 150, 'rows': 3}),
        }


class ProfissionalForm(forms.ModelForm):
    class Meta:
        model = Perfil
        fields = ['profissao', 'documento_verificacao']
        labels = {
            'profissao': 'Sou profissional',
            'documento_verificacao': 'Documento de verificação (registro no conselho)',
        }

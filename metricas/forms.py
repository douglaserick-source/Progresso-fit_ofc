from django import forms
from .models import MetricaCorporal , RegistroRanking


class MetricaCorporalForm(forms.ModelForm):
    class Meta:
        model = MetricaCorporal
        exclude = ['usuario', 'data_medicao']  # esses dois a view preenche sozinha


class RegistroRankingForm(forms.ModelForm):
    class Meta:
        model = RegistroRanking
        fields = ['categoria', 'valor', 'foto_comprovante']
        labels = {
            'categoria': 'Categoria',
            'valor': 'Medida (cm)',
            'foto_comprovante': 'Foto comprovando a medida',
        }
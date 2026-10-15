from django import forms
from .models import FichaAnamnese, FotoTreino


class FichaAnamneseForm(forms.ModelForm):
    dias = forms.MultipleChoiceField(
        choices=FichaAnamnese.DIA_CHOICES,
        widget=forms.CheckboxSelectMultiple,
        label='Dias disponíveis para treinar'
    )

    class Meta:
        model = FichaAnamnese
        fields = [
            'status', 'objetivo', 'tempo_minutos', 'dias',
            'exercicios_atuais', 'cargas_atuais', 'series_repeticoes_atual', 'observacoes',
        ]
        labels = {
            'status': 'Seu nível de experiência',
            'objetivo': 'Objetivo principal',
            'tempo_minutos': 'Tempo disponível por sessão (minutos)',
            'exercicios_atuais': 'Exercícios que você já pratica ou prefere',
            'cargas_atuais': 'Cargas atuais nos exercícios principais (kg)',
            'series_repeticoes_atual': 'Volume habitual (ex: 3x10, 4x12...)',
            'observacoes': 'Lesões, limitações, dores ou preferências',
        }
        widgets = {
            'exercicios_atuais': forms.Textarea(attrs={'rows': 2}),
            'cargas_atuais': forms.Textarea(attrs={'rows': 2}),
            'series_repeticoes_atual': forms.Textarea(attrs={'rows': 2}),
            'observacoes': forms.Textarea(attrs={'rows': 3}),
        }


class FotoTreinoForm(forms.ModelForm):
    class Meta:
        model = FotoTreino
        fields = ['imagem']

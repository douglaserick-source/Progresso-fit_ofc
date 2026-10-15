from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class FichaAnamnese(models.Model):
    STATUS_CHOICES = [
        ('iniciante', 'Iniciante'),
        ('intermediario', 'Intermediário'),
        ('avancado', 'Avançado'),
    ]
    OBJETIVO_CHOICES = [
        ('hipertrofia', 'Hipertrofia'),
        ('emagrecimento', 'Emagrecimento'),
        ('definicao', 'Definição/Secar'),
        ('forca', 'Força'),
        ('condicionamento', 'Condicionamento'),
    ]
    DIA_CHOICES = [
        ('Segunda', 'Segunda'), ('Terça', 'Terça'), ('Quarta', 'Quarta'),
        ('Quinta', 'Quinta'), ('Sexta', 'Sexta'), ('Sábado', 'Sábado'), ('Domingo', 'Domingo'),
    ]

    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='fichas_anamnese')
    data_submissao = models.DateTimeField(auto_now_add=True)

    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    objetivo = models.CharField(max_length=20, choices=OBJETIVO_CHOICES)
    tempo_minutos = models.PositiveSmallIntegerField(help_text='Tempo disponível por sessão, em minutos')
    dias = models.JSONField(default=list, help_text='Lista de dias da semana selecionados')

    exercicios_atuais = models.TextField(blank=True, help_text='Exercícios que já pratica ou prefere')
    cargas_atuais = models.TextField(blank=True, help_text='Cargas atuais nos exercícios principais')
    series_repeticoes_atual = models.TextField(blank=True, help_text='Volume habitual (séries x repetições)')
    observacoes = models.TextField(blank=True, help_text='Lesões, limitações, dores ou preferências')

    class Meta:
        ordering = ['-data_submissao']

    def __str__(self):
        return f'Ficha de {self.usuario.username} em {self.data_submissao.strftime("%d/%m/%Y")}'

    @property
    def dias_desde_submissao(self):
        return (timezone.now().date() - self.data_submissao.date()).days

    @property
    def precisa_reavaliacao(self):
        return self.dias_desde_submissao >= 30


class PlanoTreino(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='planos_treino')
    ficha = models.ForeignKey(FichaAnamnese, on_delete=models.CASCADE, related_name='planos')
    gerado_em = models.DateTimeField(auto_now_add=True)

    resumo = models.TextField(help_text='Resumo do plano: divisão, agrupamentos, tempo por sessão')
    conteudo = models.JSONField(help_text='Ficha detalhada: {"Segunda": [{"exercicio":...,"series":...,...}]}')
    orientacoes = models.TextField(blank=True, help_text='Cadência, aquecimento, progressão de cargas')

    class Meta:
        ordering = ['-gerado_em']

    def __str__(self):
        return f'Plano de {self.usuario.username} ({self.gerado_em.strftime("%d/%m/%Y")})'


class FotoTreino(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='fotos_treino')
    imagem = models.ImageField(upload_to='fotos_treino/')
    enviada_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-enviada_em']

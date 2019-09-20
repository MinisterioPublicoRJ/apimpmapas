from django.db import models
from colorfield.fields import ColorField


class Area(models.Model):
    nome = models.CharField(max_length=255)
    cor = ColorField(default='#FF0000')
    icone = models.ForeignKey(
        'icones.Icone',
        on_delete=models.PROTECT,
    )
    prioridade = models.IntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        if self:
            return self.nome


class Tema(models.Model):
    titulo = models.CharField(max_length=255)
    area_mae = models.ForeignKey(
        'Area',
        on_delete=models.PROTECT,
        related_name='temas',
    )
    areas_correlatas = models.ManyToManyField(
        'Area',
        related_name='temas_correlatos',
        blank=True
    )
    visivel = models.BooleanField(default=True)
    fonte_dados = models.TextField()
    tabela_pg = models.CharField(max_length=255, null=True, blank=True)
    tabela_drive = models.CharField(max_length=255, null=True, blank=True)
    subtitulo = models.CharField(max_length=255)
    descricao = models.TextField(null=True, blank=True)
    observacao = models.CharField(max_length=255, null=True, blank=True)
    url_tableau = models.URLField(max_length=255, null=True, blank=True)
    prioridade = models.IntegerField(default=1)
    dados_craai = models.BooleanField(default=True)
    dados_estado = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        if self:
            return self.titulo

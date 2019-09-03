from django.db import models
from django.utils.html import format_html
from colorfield.fields import ColorField


class Icone(models.Model):
    nome = models.CharField(max_length=255)
    image = models.TextField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.nome


class Area(models.Model):
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
=======
>>>>>>> Mprj + funcional
    nome = models.CharField(max_length=255)
=======
    nome = models.CharField(max_length=255) 
>>>>>>> Mprj + funcional
<<<<<<< HEAD
=======
=======
>>>>>>> Correção de flake8
    nome = models.CharField(max_length=255)
>>>>>>> Correção de flake8
=======
    nome = models.CharField(max_length=255) 
>>>>>>> Mprj + funcional
=======
    nome = models.CharField(max_length=255)
>>>>>>> Correção de flake8
<<<<<<< HEAD
=======
>>>>>>> Mprj + funcional
=======
>>>>>>> Correção de flake8
    cor = ColorField(default='#FF0000')
    icone = models.ForeignKey(
        Icone,
        on_delete=models.PROTECT,
    )
    prioridade = models.IntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        if self:
            return self.nome

    def color_display(self):
        return format_html(
            '<span class="color-box" style="background-color: {};">\
            </span>\
            {}',
            self.cor,
            self.cor,
        )


class Tema(models.Model):
    titulo = models.CharField(max_length=255)
    area_mae = models.ForeignKey(
        Area,
        on_delete=models.PROTECT,
        related_name='temas',
    )
    areas_correlatas = models.ManyToManyField(
        Area,
        related_name='temas_correlatos',
        blank=True
    )
    visivel = models.BooleanField(default=True)
    fonte_dados = models.TextField(null=True, blank=True)
    tabela_pg = models.CharField(max_length=255, null=True, blank=True)
    tabela_drive = models.CharField(max_length=255, null=True, blank=True)
    subtitulo = models.CharField(max_length=255, null=True, blank=True)
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

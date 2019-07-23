from django.db import models
from ordered_model.models import OrderedModel

POSTGRES = 'PG'
ORACLE = 'ORA'
BDA = 'BDA'
DATABASE_CHOICES = [
    (POSTGRES, 'PostgreSQL Opengeo'),
    (ORACLE, 'Oracle ExaData'),
    (BDA, 'Oracle BDA'),
]

TEXT_GDE = 'texto_grande'
TEXT_PEQ = 'texto_pequeno'
TEXT_PEQ_DEST = 'texto_pequeno_destaque'
LIST_UNRANK = 'lista_sem_ordenacao'
LIST_RANKED = 'lista_ordenada'
GRAPH_BAR_VERT = 'grafico_barra_vertical'
GRAPH_BAR_HORI = 'grafico_barra_horizontal'
GRAPH_PIZZA = 'grafico_pizza'
REPR_CHOICES = [
    (TEXT_GDE, 'Texto em coluna dupla'),
    (TEXT_PEQ, 'Texto em coluna simples'),
    (TEXT_PEQ_DEST, 'Texto destacado em coluna simples'),
    (LIST_UNRANK, 'Lista sem ordenação'),
    (LIST_RANKED, 'Lista ordenada'),
    (GRAPH_BAR_VERT, 'Gráfico de barras verticais'),
    (GRAPH_BAR_HORI, 'Gráfico de barras horizontais'),
    (GRAPH_PIZZA, 'Gráfico de pizza'),
]


class Icone(models.Model):
    name = models.CharField(max_length=20)
    file_path = models.FileField(upload_to='icones')

    def __str__(self):
        if self is not None:
            return self.name


class Entidade(models.Model):
    name = models.CharField(max_length=25)
    abreviation = models.CharField(max_length=3)

    database = models.CharField(
        max_length=3,
        choices=DATABASE_CHOICES,
        default=POSTGRES,
    )

    schema = models.CharField(max_length=100)
    table = models.CharField(max_length=100)
    id_column = models.CharField(max_length=200)
    name_column = models.CharField(max_length=200)
    geom_column = models.CharField(max_length=25, null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        if self is not None:
            return self.name


class Dado(OrderedModel):
    title = models.CharField(max_length=100)
    exibition_field = models.CharField(max_length=50, null=True, blank=True)
    data_type = models.CharField(
        max_length=50,
        choices=REPR_CHOICES,
        default=TEXT_GDE,
    )

    entity_type = models.ForeignKey(
        Entidade,
        on_delete=models.CASCADE,
        related_name="data_list"
    )

    database = models.CharField(
        max_length=3,
        choices=DATABASE_CHOICES,
        default=POSTGRES,
    )

    icon = models.ForeignKey(
        Icone,
        null=True,
        blank=True,
        on_delete=models.SET_NULL
    )

    schema = models.CharField(max_length=100)
    table = models.CharField(max_length=100)
    id_column = models.CharField(max_length=200)
    data_column = models.CharField(max_length=200)
    label_column = models.CharField(max_length=200, null=True, blank=True)
    source_column = models.CharField(max_length=200, null=True, blank=True)
    details_column = models.CharField(max_length=200, null=True, blank=True)
    link_column = models.CharField(max_length=200, null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        if self is not None:
            return self.title

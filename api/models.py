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
LIST_FILTER = 'lista_filtrada'
GRAPH_BAR_VERT = 'grafico_barra_vertical'
GRAPH_BAR_HORI = 'grafico_barra_horizontal'
GRAPH_BAR_HORI_STACK = 'grafico_barra_horizontal_agrupado'
GRAPH_PIZZA = 'grafico_pizza'
REPR_CHOICES = [
    (TEXT_GDE, 'Texto em coluna dupla'),
    (TEXT_PEQ, 'Texto em coluna simples'),
    (TEXT_PEQ_DEST, 'Texto destacado em coluna simples'),
    (LIST_UNRANK, 'Lista sem ordenação'),
    (LIST_RANKED, 'Lista ordenada'),
    (LIST_FILTER, 'Lista sem ordenação com filtro de busca'),
    (GRAPH_BAR_VERT, 'Gráfico de barras verticais'),
    (GRAPH_BAR_HORI, 'Gráfico de barras horizontais'),
    (GRAPH_BAR_HORI_STACK, 'Gráfico de barras horizontais agrupadas')
    (GRAPH_PIZZA, 'Gráfico de pizza'),
]


class Icone(models.Model):
    name = models.CharField(max_length=20)
    file_path = models.FileField(upload_to='icones')

    def __str__(self):
        if self:
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

    # --------------
    # Mapa
    database_mapa = models.CharField(
        max_length=3,
        choices=DATABASE_CHOICES,
        default=POSTGRES,
    )
    schema_mapa = models.CharField(max_length=100, null=True, blank=True)
    table_mapa = models.CharField(max_length=100, null=True, blank=True)
    id_column_mapa = models.CharField(max_length=200, null=True, blank=True)
    name_column_mapa = models.CharField(max_length=200, null=True, blank=True)
    geom_column_mapa = models.CharField(max_length=25, null=True, blank=True)
    entity_link_type = models.CharField(max_length=25, null=True, blank=True)
    entity_link_id_column = models.CharField(
        max_length=200,
        null=True,
        blank=True
    )

    created_at = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        if self:
            return self.name


class Mapa(models.Model):
    entity = models.OneToOneField(
        Entidade,
        on_delete=models.CASCADE,
        primary_key=True,
        related_name='map_info'
    )
    database = models.CharField(
        'Banco de dados',
        max_length=3,
        choices=DATABASE_CHOICES,
        default=POSTGRES,
    )
    schema = models.CharField('Esquema', max_length=50)
    table = models.CharField('Tabela', max_length=50)
    entity_id_column = models.CharField(
        'Coluna do ID da entidade',
        max_length=50
    )
    label_column = models.CharField('Coluna do label do mapa', max_length=50)
    geom_column = models.CharField('Coluna do json do mapa', max_length=50)
    related_entity_column = models.CharField(
        'Coluna da entidade apontada',
        max_length=50
    )
    related_id_column = models.CharField(
        'Coluna do ID apontado',
        max_length=50
    )


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
    external_link_column = models.CharField(
        max_length=200,
        null=True,
        blank=True
    )

    entity_link_type = models.ForeignKey(
        Entidade,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    entity_link_id_column = models.CharField(
        max_length=200,
        null=True,
        blank=True
    )

    created_at = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        if self:
            return self.title

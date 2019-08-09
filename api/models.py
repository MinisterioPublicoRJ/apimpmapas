from django.db import models
from colorfield.fields import ColorField
from ordered_model.models import OrderedModel

POSTGRES = 'PG'
ORACLE = 'ORA'
BDA = 'BDA'
DATABASE_CHOICES = [
    (POSTGRES, 'PostgreSQL Opengeo'),
    (ORACLE, 'Oracle ExaData'),
    (BDA, 'Oracle BDA'),
]

SINGLETON_DATA = 'Singleton'
LIST_DATA = 'List'
GRAPH_DATA = 'Graph'
SERIALIZATION_CHOICES = [
    (SINGLETON_DATA, 'Serialização para dado único'),
    (LIST_DATA, 'Serialização para lista de dados'),
    (GRAPH_DATA, 'Serialização para gráfico'),
]


class TipoDado(models.Model):
    name = models.CharField('Tipo de dado', max_length=50)
    serialization = models.CharField(
        'Forma de serialização',
        max_length=20,
        choices=SERIALIZATION_CHOICES,
        default=SINGLETON_DATA,
    )

    def __str__(self):
        if self:
            return self.name


class TemaDado(models.Model):
    name = models.CharField('Tema do dado', max_length=50)
    color = ColorField(default='#FFFFFF')

    def __str__(self):
        if self:
            return self.name


class Icone(models.Model):
    name = models.CharField('Título do ícone', max_length=20)
    file_path = models.FileField('Arquivo do ícone', upload_to='icones')

    def __str__(self):
        if self:
            return self.name


class Entidade(models.Model):
    name = models.CharField('Nome da entidade', max_length=25)
    abreviation = models.CharField('Abreviação da entidade', max_length=5)

    database = models.CharField(
        'Banco de dados',
        max_length=3,
        choices=DATABASE_CHOICES,
        default=POSTGRES,
    )

    schema = models.CharField('Esquema', max_length=100)
    table = models.CharField('Tabela', max_length=100)
    id_column = models.CharField('Coluna de ID da entidade', max_length=200)
    name_column = models.CharField(
        'Coluna de nome da entidade',
        max_length=200
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
    title = models.CharField("Titulo da caixinha", max_length=100)

    data_type = models.ForeignKey(
        TipoDado,
        on_delete=models.PROTECT,
        related_name="data_type",
        verbose_name="Tipo da caixinha"
    )

    theme = models.ForeignKey(
        TemaDado,
        on_delete=models.SET_NULL,
        related_name="data_by_theme",
        verbose_name="Tema da caixinha",
        null=True
    )

    entity_type = models.ForeignKey(
        Entidade,
        on_delete=models.CASCADE,
        related_name="data_list",
        verbose_name="Entidade relacionada"
    )

    database = models.CharField(
        'Banco de dados',
        max_length=3,
        choices=DATABASE_CHOICES,
        default=POSTGRES,
    )

    icon = models.ForeignKey(
        Icone,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        verbose_name="Ícone"
    )

    schema = models.CharField("Esquema", max_length=100)
    table = models.CharField("Tabela", max_length=100)
    id_column = models.CharField("Coluna do ID da Entidade", max_length=200)
    data_column = models.CharField(
        "Coluna da informação principal exibida",
        max_length=200
    )
    label_column = models.CharField(
        "Coluna de rótulo dos dados",
        max_length=200,
        null=True,
        blank=True
    )
    source_column = models.CharField(
        "Coluna de fonte dos dados",
        max_length=200,
        null=True,
        blank=True
    )
    details_column = models.CharField(
        "Coluna de detalhes sobre os dados",
        max_length=200,
        null=True,
        blank=True
    )
    image_column = models.CharField(
        "Coluna de imagem",
        max_length=200,
        null=True,
        blank=True
    )
    external_link_column = models.CharField(
        "Coluna de link externo",
        max_length=200,
        null=True,
        blank=True
    )

    entity_link_type = models.ForeignKey(
        Entidade,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Entidade apontada em link interno"
    )

    entity_link_id_column = models.CharField(
        "Coluna de ID da entidade apontada",
        max_length=200,
        null=True,
        blank=True
    )

    limit_fetch = models.IntegerField(
        'Máximo de dados a serem mostrados',
        default=0,
        help_text='0 = sem limite'
    )

    order_with_respect_to = 'entity_type'

    created_at = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        if self:
            return self.title

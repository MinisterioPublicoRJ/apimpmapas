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


class Coluna(models.Model):
    # CHOICES
    ID_COLUMN = 'id'
    LABEL_COLUMN = 'label'
    INTERNAL_ENTITY_COLUMN = 'entidade interna'
    INTERNAL_ID_COLUMN = 'id interna'
    BASE_CHOICES = [
        (ID_COLUMN, 'Coluna de ID da entidade'),
        (LABEL_COLUMN, 'Coluna de rótulo dos dados'),
        (INTERNAL_ENTITY_COLUMN, 'Coluna de tipo de entidade vinculada'),
        (INTERNAL_ID_COLUMN, 'Coluna de id de entidade vinculada'),
    ]
    INFO_CHOICES = []

    # DATABASE FIELDS
    name = models.CharField(
        verbose_name='nome da coluna na tabela',
        max_length=200,
    )

    info_type = models.CharField(
        verbose_name='tipo de informação da coluna',
        max_length=50,
        choices=INFO_CHOICES,
        default=ID_COLUMN,
        blank=False,
        help_text='''<pre>Toda caixinha e mapa precisa de uma coluna de id
        Toda caixinha precisa de uma coluna de dados
        Todo mapa precisa de uma coluna de geojson, contendo um mapa em formato geojson
        Caixinhas de gráficos precisam de uma coluna do tipo label
        Colunas de imagem precisam referenciar um campo do tipo "BLOB"
        Colunas de tipo e id de entidade vinculada precisam existir aos pares</pre>'''
    )

    created_at = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)


class ColunaDado(Coluna):
    # CHOICES
    DATA_COLUMN = 'data'
    SOURCE_COLUMN = 'source'
    IMAGE_COLUMN = 'image'
    EXTERNAL_LINK_COLUMN = 'link externo'
    INFO_CHOICES = Coluna.BASE_CHOICES + [
        (DATA_COLUMN, 'Coluna de dados principais'),
        (SOURCE_COLUMN, 'Coluna de fonte dos dados'),
        (IMAGE_COLUMN, 'Coluna de imagem'),
        (EXTERNAL_LINK_COLUMN, 'Coluna de link externo'),
    ]


class ColunaMapa(Coluna):
    # CHOICES
    GEOJSON_COLUMN = 'geojson'
    INFO_CHOICES = Coluna.BASE_CHOICES + [
        (GEOJSON_COLUMN, 'Coluna de json do mapa'),
    ]


class TipoDado(models.Model):
    # CHOICES
    SINGLETON_DATA = 'Singleton'
    LIST_DATA = 'List'
    XY_GRAPH_DATA = 'Graph'
    PIZZA_GRAPH_DATA = 'Pizza'
    SERIALIZATION_CHOICES = [
        (SINGLETON_DATA, 'Serialização para dado único'),
        (LIST_DATA, 'Serialização para lista de dados'),
        (XY_GRAPH_DATA, 'Serialização para gráfico cartesiano'),
        (PIZZA_GRAPH_DATA, 'Serialização para gráfico de pizza'),
    ]

    # DATABASE FIELDS
    name = models.CharField(
        verbose_name='tipo de dado',
        max_length=50
    )

    serialization = models.CharField(
        verbose_name='forma de serialização',
        max_length=20,
        choices=SERIALIZATION_CHOICES,
        default=SINGLETON_DATA,
    )

    # META CLASS
    class Meta:
        verbose_name = 'tipo de dados'
        verbose_name_plural = 'tipos de dados'

    # TO STRING METHOD
    def __str__(self):
        if self:
            return self.name


class TemaDado(models.Model):
    # DATABASE FIELDS
    name = models.CharField(
        verbose_name='tema do dado',
        max_length=50
    )

    color = ColorField(
        verbose_name='cor das caixinhas',
        default='#FFFFFF'
    )

    # META CLASS
    class Meta:
        verbose_name = 'tema de dados'
        verbose_name_plural = 'temas de dados'

    # TO STRING METHOD
    def __str__(self):
        if self:
            return self.name


class Icone(models.Model):
    # DATABASE FIELDS
    name = models.CharField(
        verbose_name='título do ícone',
        max_length=20
    )

    file_path = models.FileField(
        verbose_name='arquivo do ícone',
        upload_to='icones'
    )

    # META CLASS
    class Meta:
        verbose_name = 'ícone'

    # TO STRING METHOD
    def __str__(self):
        if self:
            return self.name


class Entidade(models.Model):
    # DATABASE FIELDS
    name = models.CharField(
        verbose_name='nome da entidade',
        max_length=25
    )

    abreviation = models.CharField(
        verbose_name='abreviação da entidade',
        max_length=5
    )

    database = models.CharField(
        verbose_name='banco de dados',
        max_length=3,
        choices=DATABASE_CHOICES,
        default=POSTGRES,
    )

    schema = models.CharField(
        verbose_name='esquema',
        max_length=100
    )

    table = models.CharField(
        verbose_name='tabela',
        max_length=100
    )

    id_column = models.CharField(
        verbose_name='coluna de ID da entidade',
        max_length=200
    )

    name_column = models.CharField(
        verbose_name='coluna de nome da entidade',
        max_length=200
    )

    created_at = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)

    # TO STRING METHOD
    def __str__(self):
        if self:
            return self.name


class Mapa(models.Model):
    # DATABASE FIELDS
    entity = models.OneToOneField(
        Entidade,
        on_delete=models.CASCADE,
        primary_key=True,
        related_name='map_info'
    )

    database = models.CharField(
        verbose_name='banco de dados',
        max_length=3,
        choices=DATABASE_CHOICES,
        default=POSTGRES,
    )

    schema = models.CharField(
        verbose_name='esquema',
        max_length=50
    )

    table = models.CharField(
        verbose_name='tabela',
        max_length=50
    )

    columns = models.ManyToManyField(ColunaMapa)

    entity_id_column = models.CharField(
        verbose_name='coluna do ID da entidade',
        max_length=50
    )

    label_column = models.CharField(
        verbose_name='coluna do label do mapa',
        max_length=50
    )

    geom_column = models.CharField(
        verbose_name='coluna do json do mapa',
        max_length=50
    )

    related_entity_column = models.CharField(
        verbose_name='coluna da entidade apontada',
        max_length=50
    )

    related_id_column = models.CharField(
        verbose_name='coluna do ID apontado',
        max_length=50
    )


class Dado(OrderedModel):
    # DATABASE FIELDS
    title = models.CharField(
        verbose_name='titulo da caixinha',
        max_length=100
    )

    exibition_field = models.CharField(
        verbose_name='nome de exibição da caixinha',
        max_length=100,
        null=True,
        blank=True,
        help_text='Não obrigatório'
    )

    data_type = models.ForeignKey(
        TipoDado,
        on_delete=models.PROTECT,
        related_name="data_by_type",
        verbose_name="tipo da caixinha"
    )

    theme = models.ForeignKey(
        TemaDado,
        on_delete=models.SET_NULL,
        related_name="data_by_theme",
        verbose_name="tema da caixinha",
        null=True
    )

    entity_type = models.ForeignKey(
        Entidade,
        on_delete=models.CASCADE,
        related_name="data_list",
        verbose_name="entidade relacionada"
    )

    database = models.CharField(
        verbose_name='banco de dados',
        max_length=3,
        choices=DATABASE_CHOICES,
        default=POSTGRES,
    )

    icon = models.ForeignKey(
        Icone,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        verbose_name="ícone"
    )

    schema = models.CharField(
        verbose_name='esquema',
        max_length=100
    )

    table = models.CharField(
        verbose_name='tabela',
        max_length=100
    )

    columns = models.ManyToManyField(ColunaDado)

    id_column = models.CharField(
        verbose_name='coluna do ID da Entidade',
        max_length=200
    )

    data_column = models.CharField(
        verbose_name='coluna da informação principal exibida',
        max_length=200
    )

    label_column = models.CharField(
        verbose_name='coluna de rótulo dos dados',
        max_length=200,
        null=True,
        blank=True
    )

    source_column = models.CharField(
        verbose_name='coluna de fonte dos dados',
        max_length=200,
        null=True,
        blank=True
    )

    details_column = models.CharField(
        verbose_name='coluna de detalhes sobre os dados',
        max_length=200,
        null=True,
        blank=True
    )

    image_column = models.CharField(
        verbose_name='coluna de imagem',
        max_length=200,
        null=True,
        blank=True
    )

    external_link_column = models.CharField(
        verbose_name='coluna de link externo',
        max_length=200,
        null=True,
        blank=True
    )

    entity_link_type = models.ForeignKey(
        Entidade,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="entidade apontada em link interno"
    )

    entity_link_id_column = models.CharField(
        verbose_name='coluna de ID da entidade apontada',
        max_length=200,
        null=True,
        blank=True
    )

    limit_fetch = models.IntegerField(
        verbose_name='máximo de dados a serem mostrados',
        default=0,
        help_text='0 = sem limite'
    )

    created_at = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)

    # CONFIG FIELDS
    order_with_respect_to = 'entity_type'

    # TO STRING METHOD
    def __str__(self):
        if self:
            return self.title

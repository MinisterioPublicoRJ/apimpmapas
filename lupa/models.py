from django.core.exceptions import ValidationError
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

BLANK = ('', '--------')

SUBURB = 'suburb'
MUNICIPALITY = 'municipality'
OSM_VALUES_CHOICES = (
    (SUBURB, 'Bairro'),
    (MUNICIPALITY, 'Município')
)


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

    created_at = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)

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
        default='#000000'
    )

    created_at = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)

    # META CLASS
    class Meta:
        verbose_name = 'tema de dados'
        verbose_name_plural = 'temas de dados'

    # TO STRING METHOD
    def __str__(self):
        if self:
            return self.name


class Grupo(models.Model):
    # DATABASE FIELDS
    name = models.CharField(
        verbose_name='nome do grupo',
        max_length=50
    )

    role = models.CharField(
        verbose_name='role no SCA',
        max_length=100
    )

    created_at = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)

    # META CLASS
    class Meta:
        verbose_name = 'grupo de usuários'
        verbose_name_plural = 'grupos de usuários'

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

    created_at = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)

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

    roles_allowed = models.ManyToManyField(
        Grupo,
        related_name="entity_allowed",
        verbose_name="grupos com acesso",
        blank=True,
        help_text='Deixar em branco para todos',
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

    geojson_column = models.CharField(
        verbose_name='coluna de dados geojson da entidade',
        max_length=200,
        null=True,
        blank=True
    )

    osm_value_attached = models.CharField(
        verbose_name='TAG osm_values atrelada',
        max_length=50,
        null=True,
        blank=True,
        choices=OSM_VALUES_CHOICES
    )

    osm_default_level = models.BooleanField(
        verbose_name='busca de geolocalização padrão',
        default=False
    )

    def clean(self):
        errors = {}
        has_osm_value = 'A Entidade %s já possui a propriedade %s'
        has_osm_default = ('A Entidade %s já responde pela'
                           ' busca padrão de geolocalização')

        if self.osm_value_attached:
            pc = Entidade.objects.filter(
                osm_value_attached=self.osm_value_attached
            ).first()
            if pc:
                errors['osm_value_attached'] = ValidationError(
                    has_osm_value % (pc.name, pc.osm_value_attached),
                    code="invalid"
                )

        if self.osm_default_level:
            pc = Entidade.objects.filter(
                osm_default_level=True
            ).first()
            if pc:
                errors['osm_default_level'] = ValidationError(
                    has_osm_default % pc.name,
                    code="invalid"
                )

        if errors:
            raise ValidationError(errors)

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

    created_at = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)


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
        null=True,
        blank=True
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

    roles_allowed = models.ManyToManyField(
        Grupo,
        related_name="data_allowed",
        verbose_name="grupos com acesso",
        blank=True,
        help_text='Deixar em branco para todos',
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


class Coluna(models.Model):
    # CLASS FIELDS
    help_info_type = '''<pre>Toda caixinha e mapa precisa de uma coluna de id
Toda caixinha precisa de uma coluna de dados
Todo mapa precisa de uma coluna de geojson, contendo a string json de um mapa
Caixinhas de gráficos precisam de uma coluna do tipo label
Colunas de imagem precisam referenciar um campo do tipo "BLOB"
Colunas de tipo e id de entidade vinculada precisam existir aos pares</pre>'''

    # CHOICES
    ID_COLUMN = 'id'
    LABEL_COLUMN = 'rotulo'
    INTERNAL_ENTITY_COLUMN = 'entidade_interna'
    INTERNAL_ID_COLUMN = 'id_interna'
    BASE_CHOICES = [
        BLANK,
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
        blank=False
    )

    created_at = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)

    # META CLASS
    class Meta:
        abstract = True


class ColunaDado(Coluna):
    # CHOICES
    DATA_COLUMN = 'dado'
    SOURCE_COLUMN = 'source'
    IMAGE_COLUMN = 'imagem'
    EXTERNAL_LINK_COLUMN = 'link_externo'
    TITLE_SUFFIX_COLUMN = 'sufixo_titulo'
    DETAIL_COLUMN = 'details'
    INFO_CHOICES = Coluna.BASE_CHOICES + [
        (DATA_COLUMN, 'Coluna de dados principais'),
        (SOURCE_COLUMN, 'Coluna de fonte dos dados'),
        (IMAGE_COLUMN, 'Coluna de imagem'),
        (EXTERNAL_LINK_COLUMN, 'Coluna de link externo'),
        (TITLE_SUFFIX_COLUMN, 'Coluna de sufixo no titulo'),
        (DETAIL_COLUMN, 'Detalhes')
    ]

    dado = models.ForeignKey(
        Dado,
        on_delete=models.CASCADE,
        related_name="column_list",
        verbose_name="dado"
    )


class ColunaMapa(Coluna):
    # CHOICES
    GEOJSON_COLUMN = 'geojson'
    INFO_CHOICES = Coluna.BASE_CHOICES + [
        (GEOJSON_COLUMN, 'Coluna de json do mapa'),
    ]

    mapa = models.ForeignKey(
        Mapa,
        on_delete=models.CASCADE,
        related_name="column_list",
        verbose_name="mapa"
    )

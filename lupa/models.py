import datetime as dt

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

HAS_OSM_VALUE = 'A Entidade %s já possui a propriedade %s'
HAS_OSM_DEFAULT = (
    'A Entidade %s já responde pela '
    'busca padrão de geolocalização')
MANDATORY_OSM_PARAMETERS = (
    'Para informar parâmetros de busca OSM é necessário '
    'informar a Coluna de Dados GEOJSON'
)
MANDATORY_GEOJSON_COLUMN = (
    'Para informar coluna GEOJSON é necessário informar '
    'corretamente os parâmetros OSM'
)
ONLY_POSTGIS_SUPORTED = (
    'Apenas a engine PostgreSQL Opengeo suporta busca geolocalizada'
)


class CacheManager(models.Manager):
    def to_days(self, seconds):
        return seconds / 60 / 60 / 24

    def expiring(self):
        objs = super().get_queryset()
        result_ids = []
        for obj in objs:
            cache_days = self.to_days(obj.cache_timeout)
            timedelta = dt.date.today() - dt.timedelta(days=cache_days)
            if obj.last_cache_update is None\
                    or obj.last_cache_update <= timedelta:
                result_ids.append(obj.id)

        return objs.filter(id__in=result_ids)


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
        'Grupo',
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
        verbose_name='coluna de dados GEOJSON da entidade',
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

    is_cacheable = models.BooleanField(
        verbose_name='guardar no cache?',
        default=True
    )
    cache_timeout = models.BigIntegerField(
        verbose_name='Tempo de persistência do cache (em dias)',
        default=7
    )
    last_cache_update = models.DateField(null=True)
    objects = models.Manager()
    cache = CacheManager()

    def obter_dados(self):
        return self.data_list.order_by('order')

    def clean(self):
        errors = {}

        if not self.geojson_column and (
                    self.osm_value_attached or self.osm_default_level
                ):
            errors['geojson_column'] = ValidationError(
                MANDATORY_OSM_PARAMETERS,
                code="invalid"
            )

        if self.geojson_column and not (
                    self.osm_value_attached or self.osm_default_level
                ):
            errors['geojson_column'] = ValidationError(
                MANDATORY_GEOJSON_COLUMN,
                code="invalid"
            )

        if self.osm_value_attached:
            pc = Entidade.objects.filter(
                osm_value_attached=self.osm_value_attached
            ).exclude(id=self.id).first()
            if pc:
                errors['osm_value_attached'] = ValidationError(
                    HAS_OSM_VALUE % (
                        pc.name,
                        dict(OSM_VALUES_CHOICES)[pc.osm_value_attached]
                    ),
                    code="invalid"
                )

        if self.osm_default_level:
            pc = Entidade.objects.filter(
                osm_default_level=True
            ).exclude(id=self.id).first()
            if pc:
                errors['osm_default_level'] = ValidationError(
                    HAS_OSM_DEFAULT % pc.name,
                    code="invalid"
                )

        if self.geojson_column and self.database != POSTGRES:
            errors['geojson_column'] = ValidationError(
                ONLY_POSTGIS_SUPORTED,
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

    def save(self, *args, **kwargs):
        seconds_scale = 24 * 60 * 60
        self.cache_timeout = self.cache_timeout * seconds_scale
        super().save(*args, **kwargs)


class Mapa(models.Model):
    # DATABASE FIELDS
    entity = models.OneToOneField(
        'Entidade',
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

    database = models.CharField(
        verbose_name='banco de dados',
        max_length=3,
        choices=DATABASE_CHOICES,
        default=POSTGRES,
    )

    icon = models.ForeignKey(
        'icones.Icone',
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

    show_box = models.BooleanField(
        verbose_name='Exibir dado',
        default=True
    )

    is_cacheable = models.BooleanField(
        verbose_name='guardar no cache?',
        default=True
    )

    cache_timeout = models.BigIntegerField(
        verbose_name='Tempo de persistência do cache (em dias)',
        default=7
    )

    last_cache_update = models.DateField(null=True)
    cache = CacheManager()

    created_at = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)

    class Meta(OrderedModel.Meta):
        abstract = True

    # TO STRING METHOD
    def __str__(self):
        if self:
            return self.title

    def save(self, *args, **kwargs):
        seconds_scale = 24 * 60 * 60
        self.cache_timeout = self.cache_timeout * seconds_scale
        super().save(*args, **kwargs)


class DadoEntidade(Dado):
    data_type = models.ForeignKey(
        'TipoDado',
        on_delete=models.PROTECT,
        related_name="data_by_type",
        verbose_name="tipo da caixinha"
    )

    entity_type = models.ForeignKey(
        'Entidade',
        on_delete=models.CASCADE,
        related_name="data_list",
        verbose_name="entidade relacionada"
    )

    theme = models.ForeignKey(
        'TemaDado',
        on_delete=models.SET_NULL,
        related_name="data_by_theme",
        verbose_name="tema da caixinha",
        null=True,
        blank=True
    )

    roles_allowed = models.ManyToManyField(
        'Grupo',
        related_name="data_allowed",
        verbose_name="grupos com acesso",
        blank=True,
        help_text='Deixar em branco para todos',
    )

    show_box = models.BooleanField(
        verbose_name='exibir dado',
        default=True
    )

    # CONFIG FIELDS
    order_with_respect_to = 'entity_type'

    class Meta:
        verbose_name = 'dado'


class DadoDetalhe(Dado):
    data_type = models.ForeignKey(
        'TipoDado',
        on_delete=models.PROTECT,
        related_name="details_by_type",
        verbose_name="tipo do detalhe"
    )

    dado_main = models.ForeignKey(
        'DadoEntidade',
        on_delete=models.CASCADE,
        related_name='data_details',
        verbose_name='detalhes'
    )

    # CONFIG FIELDS
    order_with_respect_to = 'dado_main'


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
    IMAGE_LINK_COLUMN = 'linkimagem'
    EXTERNAL_LINK_COLUMN = 'link_externo'
    TITLE_SUFFIX_COLUMN = 'sufixo_titulo'
    DETAIL_COLUMN = 'details'
    INFO_CHOICES = Coluna.BASE_CHOICES + [
        (DATA_COLUMN, 'Coluna de dados principais'),
        (SOURCE_COLUMN, 'Coluna de fonte dos dados'),
        (IMAGE_COLUMN, 'Coluna de imagem'),
        (IMAGE_LINK_COLUMN, 'Coluna de Link de Imagem'),
        (EXTERNAL_LINK_COLUMN, 'Coluna de link externo'),
        (TITLE_SUFFIX_COLUMN, 'Coluna de sufixo no titulo'),
        (DETAIL_COLUMN, 'Detalhes')
    ]

    dado = models.ForeignKey(
        'DadoEntidade',
        on_delete=models.CASCADE,
        related_name="column_list",
        verbose_name="dado"
    )


class ColunaDetalhe(Coluna):
    # Sim, eu sei que essa classe é idêntica à ColunaDado
    # O que fiz, eu fiz sem escolha. Em nome da paz e da sanidade
    # Mas não em nome do Doutor

    # CHOICES
    DATA_COLUMN = 'dado'
    SOURCE_COLUMN = 'source'
    IMAGE_COLUMN = 'imagem'
    IMAGE_LINK_COLUMN = 'linkimagem'
    EXTERNAL_LINK_COLUMN = 'link_externo'
    TITLE_SUFFIX_COLUMN = 'sufixo_titulo'
    DETAIL_COLUMN = 'details'
    INFO_CHOICES = Coluna.BASE_CHOICES + [
        (DATA_COLUMN, 'Coluna de dados principais'),
        (SOURCE_COLUMN, 'Coluna de fonte dos dados'),
        (IMAGE_COLUMN, 'Coluna de imagem'),
        (IMAGE_LINK_COLUMN, 'Coluna de Link de Imagem'),
        (EXTERNAL_LINK_COLUMN, 'Coluna de link externo'),
        (TITLE_SUFFIX_COLUMN, 'Coluna de sufixo no titulo'),
        (DETAIL_COLUMN, 'Detalhes')
    ]

    dado = models.ForeignKey(
        'DadoDetalhe',
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
        'Mapa',
        on_delete=models.CASCADE,
        related_name="column_list",
        verbose_name="mapa"
    )

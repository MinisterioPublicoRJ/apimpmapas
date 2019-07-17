from django.db import models

ESTADO = 'EST'
MUNICIPIO = 'MUN'
ORGAO = 'ORG'

ENTITY_CHOICES = [
    (ESTADO, 'Estado'),
    (MUNICIPIO, 'Município'),
    (ORGAO, 'Órgão'),
]

POSTGRES = 'PG'
ORACLE = 'ORA'
BDA = 'BDA'
DATABASE_CHOICES = [
    (POSTGRES, 'PostgreSQL Opengeo'),
    (ORACLE, 'Oracle ExaData'),
    (BDA, 'Oracle BDA'),
]

TEXT_GDE = 'TEX_GDE'
TEXT_PEQ = 'TEX_PEQ'
TEXT_PEQ_DEST = 'TEX_PEQ_DEST'
DATA_CHOICES = [
    (TEXT_GDE, 'Texto em coluna dupla'),
    (TEXT_PEQ, 'Texto em coluna simples'),
    (TEXT_PEQ_DEST, 'Texto destacado em coluna simples'),
]


class Icone(models.Model):
    name = models.CharField(max_length=20)
    file_path = models.FileField(upload_to='icones')

    def __str__(self):
        if self is not None:
            return self.name


class Entidade(models.Model):
    # ID único da entidade para correspondência com o banco externo
    domain_id = models.CharField(max_length=20)
    title = models.CharField(max_length=100)
    exibition_field = models.CharField(max_length=100, null=True, blank=True)
    entity_type = models.CharField(
        max_length=3,
        choices=ENTITY_CHOICES,
        default=ORGAO,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        if self is not None:
            return self.title


class Dado(models.Model):
    title = models.CharField(max_length=100)
    exibition_field = models.CharField(max_length=50, null=True, blank=True)
    data_type = models.CharField(
        max_length=20,
        choices=DATA_CHOICES,
        default=TEXT_GDE,
    )
    entity_type = models.CharField(
        max_length=3,
        choices=ENTITY_CHOICES,
        default=ORGAO,
    )
    database = models.CharField(
        max_length=3,
        choices=DATABASE_CHOICES,
        default=POSTGRES,
    )

    icon = models.ForeignKey(
        'Icone',
        null=True,
        blank=True,
        on_delete=models.SET_NULL
    )

    schema = models.CharField(max_length=100)
    table = models.CharField(max_length=100)
    data_column = models.CharField(max_length=200)
    id_column = models.CharField(max_length=200)
    source_column = models.CharField(max_length=200, null=True, blank=True)
    details_column = models.CharField(max_length=200, null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        if self is not None:
            return self.title

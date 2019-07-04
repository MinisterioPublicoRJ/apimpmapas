from django.contrib.postgres.fields import ArrayField
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

NUMBER = 'NUM'
TEXT = 'TEX'
GRAPH = 'GRA'
MAP = 'MAP'
DATA_CHOICES = [
    (NUMBER, 'Número'),
    (TEXT, 'Texto'),
    (GRAPH, 'Gráfico'),
    (MAP, 'Mapa'),
]


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
        max_length=3,
        choices=DATA_CHOICES,
        default=TEXT,
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
    schema = models.CharField(max_length=100, null=True, blank=True)
    table = models.CharField(max_length=100)
    columns = ArrayField(
        models.CharField(max_length=50)
    )
    id_column = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        if self is not None:
            return self.title

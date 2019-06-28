from django.db import models
from django.contrib.gis.db import models as gis_models

ESTADO = 'EST'
MUNICIPIO = 'MUN'
ORGAO = 'ORG'
ENTITY_CHOICES = [
    (ESTADO, 'Estado'),
    (MUNICIPIO, 'Município'),
    (ORGAO, 'Órgão'),
]


class Entidade(models.Model):
    domain_id = models.CharField(max_length=20)  # ID único da entidade para correspondência com o banco externo
    title = models.CharField(max_length=100)
    exibition_field = models.CharField(max_length=100, null=True, blank=True)
    entity_type = models.CharField(
        max_length=3,
        choices=ENTITY_CHOICES,
        default=ORGAO,
    )
    geometry = gis_models.GeometryField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class Dado(models.Model):
    DATABASE_CHOICES = [
        ('PG', 'PostgreSQL Opengeo'),
        ('ORA', 'Oracle ExaData'),
        ('BDA', 'Oracle BDA'),
    ]

    DATA_CHOICES = [
        ('NUM', 'Número'),
        ('TEX', 'Texto'),
        ('GRA', 'Gráfico'),
    ]

    title = models.CharField(max_length=100)
    exibition_field = models.CharField(max_length=50, null=True, blank=True)
    data_type = models.CharField(
        max_length=3,
        choices=DATA_CHOICES,
        default='TEX',
    )
    entity_type = models.CharField(
        max_length=3,
        choices=ENTITY_CHOICES,
        default=ORGAO,
    )
    database = models.CharField(
        max_length=3,
        choices=DATABASE_CHOICES,
        default='PG',
    )
    query = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

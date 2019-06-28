from django.db import models
from django.contrib.gis.db import models as gis_models


class TipoEntidade(models.Model):
    name = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class TipoDado(models.Model):
    name = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Entidade(models.Model):
    domain_id = models.CharField(max_length=20)  # ID único da entidade para correspondência com o banco externo
    title = models.CharField(max_length=100)
    entity_type = models.ForeignKey(
        'TipoEntidade',
        on_delete=models.PROTECT
    )
    geometry = gis_models.GeometryField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.entity_type.name + ' - ' + self.title


class Dado(models.Model):
    POSTGRESQL = 'PG'
    ORACLE = 'ORA'
    BDA = 'BDA'
    DATABASE_CHOICES = [
        (POSTGRESQL, 'PostgreSQL Opengeo'),
        (ORACLE, 'Oracle ExaData'),
        (BDA, 'Oracle BDA'),
    ]
    title = models.CharField(max_length=100)
    exibition_field = models.CharField(max_length=50, null=True, blank=True)
    data_type = models.ForeignKey(
        'TipoDado',
        on_delete=models.PROTECT
    )
    entity_type = models.ForeignKey(
        'TipoEntidade',
        on_delete=models.CASCADE
    )
    database = models.CharField(
        max_length=3,
        choices=DATABASE_CHOICES,
        default=POSTGRESQL,
    )
    query = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

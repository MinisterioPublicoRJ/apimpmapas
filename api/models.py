from django.db import models
from django.contrib.gis.db import models as gis_models


class TipoEntidadeModel(models.Model):
    name = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)


class EntidadeModel(models.Model):
    title = models.CharField(max_length=100)
    entity_type = models.ForeignKey(
        'TipoEntidadeModel',
        on_delete=models.PROTECT
    )
    geometry = gis_models.GeometryField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)


class DadoModel(models.Model):
    pass

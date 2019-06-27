from django.db import models
from django.contrib.gis.db import models as gis_models


class TipoEntidadeModel(models.Model):
    name = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class TipoDadoModel(models.Model):
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

    def __str__(self):
        return self.entity_type.name + ' - ' + self.title


class DadoModel(models.Model):
    title = models.CharField(max_length=100)
    data_type = models.ForeignKey(
        'TipoDadoModel',
        on_delete=models.PROTECT
    )
    entity = models.ForeignKey(
        'EntidadeModel',
        on_delete=models.CASCADE
    )
    created_at = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)

from django.db import models

# Create your models here.


class Documento(models.Model):
    docu_dk = models.IntegerField(primary_key=True)
    num_mp = models.CharField(max_length=15, db_column='docu_nr_mp')
    classe = models.ForeignKey(
        'DoctoClasse',
        null=True,
        db_column='docu_cldc_dk',
        on_delete=models.SET_NULL
    )

    class Meta:
        db_table = 'MCPR_DOCUMENTO'
        managed = False


class DoctoClasse(models.Model):
    cldc_dk = models.IntegerField(primary_key=True)
    descricao = models.CharField(max_length=150, db_column='cldc_ds_classe')

    class Meta:
        db_table = 'MCPR_CLASSE_DOCTO_MP'
        managed = False

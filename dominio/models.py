from django.db import models

from .managers import VistaManager

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


class Vista(models.Model):
    vistas = VistaManager()

    vist_dk = models.IntegerField(primary_key=True)
    responsavel = models.ForeignKey(
        'PessoaFisica',
        db_column='VIST_PESF_PESS_DK_RESP_ANDAM',
        on_delete=models.SET_NULL,
        related_name='vistas',
        null=True
    )
    data_fechamento = models.DateField(
        null=True,
        db_column='VIST_DT_FECHAMENTO_VISTA'
    )
    orgao = models.ForeignKey(
        'Orgao',
        db_column='VIST_ORGI_ORGA_DK',
        on_delete=models.SET_NULL,
        related_name='vistas',
        null=True
    )

    class Meta:
        db_table = 'MCPR_VISTA'
        managed = False


class PessoaFisica(models.Model):
    pesf_pess_dk = models.IntegerField(primary_key=True)
    nome = models.CharField(
        max_length=145,
        db_column='PESF_NM_PESSOA_FISICA',
        null=True
    )
    cpf = models.CharField(max_length=11, db_column='PESF_CPF', null=True)

    class Meta:
        db_table = 'MCPR_PESSOA_FISICA'
        managed = False


class Orgao(models.Model):
    orgi_dk = models.IntegerField(primary_key=True)
    nome = models.CharField(
        max_length=145,
        db_column='ORGI_NM_ORGAO'
    )

    class Meta:
        db_table = 'ORGI_ORGAO'
        managed = False

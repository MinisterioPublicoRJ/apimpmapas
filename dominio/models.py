from django.db import models

from .managers import (
    VistaManager,
    InvestigacoesManager,
    ProcessosManager,
    FinalizadosManager,
)

# Create your models here.


class Documento(models.Model):
    objects = models.Manager()
    investigacoes = InvestigacoesManager()
    processos = ProcessosManager()

    docu_dk = models.IntegerField(primary_key=True)
    num_mp = models.CharField(max_length=15, db_column='docu_nr_mp')
    docu_tpst_dk = models.IntegerField(
        db_column='DOCU_TPST_DK'
    )
    docu_orgi_orga_dk_responsavel = models.IntegerField(
        db_column="DOCU_ORGI_ORGA_DK_RESPONSAVEL",
        null=True
    )
    docu_orgi_orga_dk_carga = models.IntegerField(
        db_column="DOCU_ORGI_ORGA_DK_CARGA",
        null=True
    )
    docu_orgi_orga_dk_responsavel = models.IntegerField(
        db_column="DOCU_ORGI_ORGA_DK_RESPONSAVEL",
        null=True
    )
    docu_cldc_dk = models.IntegerField(
        db_column="DOCU_CLDC_DK",
        null=True
    )
    docu_fsdc_dk = models.IntegerField(
        db_column="DOCU_FSDC_DK",
    )
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
    objects = models.Manager()
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
    data_abertura = models.DateField(
        db_column='VIST_DT_ABERTURA_VISTA'
    )

    documento = models.ForeignKey(
        'Documento',
        db_column='VIST_DOCU_DK',
        on_delete=models.SET_NULL,
        related_name="documentos",
        null=True,
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


class Andamento(models.Model):
    pcao_dk = models.IntegerField(primary_key=True)
    pcao_dt_andamento = models.DateField(
        db_column="PCAO_DT_ANDAMENTO"
    )

    vista = models.ForeignKey(
        "Vista",
        db_column="PCAO_VIST_DK",
        on_delete=models.SET_NULL,
        null=True
    )

    class Meta:
        db_table = 'MCPR_ANDAMENTO'
        managed = False


class SubAndamento(models.Model):
    finalizados = FinalizadosManager()

    stao_dk = models.IntegerField(primary_key=True)
    stao_tppr_dk = models.IntegerField(
        db_column="STAO_TPPR_DK",
    )

    andamento = models.ForeignKey(
        "Andamento",
        db_column="STAO_PCAO_DK",
        on_delete=models.SET_NULL,
        null=True
    )

    class Meta:
        db_table = "MCPR_SUB_ANDAMENTO"
        managed = False

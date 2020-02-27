from datetime import date, timedelta

from django.db import models
from django.db.models import (
    Case,
    Q,
    F,
    ExpressionWrapper,
    Value,
    Sum,
    When
)


class VistaManager(models.Manager):
    def abertas(self):
        return self.get_queryset().filter(
            Q(data_fechamento=None) |
            Q(data_fechamento__gt=date.today())
        )

    def abertas_promotor(self, orgao_id, cpf):
        """Busca o número de vistas abertas para um dado órgão e matrícula
        na base do Oracle.

        Arguments:
            orgao_id {integer} -- ID do órgão a ser procurado.
            cpf {String} -- cpf do usuário detentor das vistas.

        Returns:
            List[Tuple] -- Lista com o resultado da query.
        """
        return self.abertas().filter(
            Q(documento__docu_orgi_orga_dk_responsavel=orgao_id) |
            Q(documento__docu_orgi_orga_dk_carga=orgao_id),
            responsavel__cpf=cpf
        ).exclude(documento__docu_tpst_dk=11)

    def abertas_por_dias_abertura(self, orgao_id, cpf):
        """
        Busca o número de vistas abertas para um um dado órgão e matrícula
        agrupadas com a contagem de dias que estão abertas

        Arguments:
            orgao_id {integer} -- ID do órgão a ser procurado.
            cpf {String} -- cpf do usuário detentor das vistas.
        """

        queryset = self.abertas_promotor(orgao_id, cpf).annotate(
            dias_abertura=ExpressionWrapper(
                date.today() - F('data_abertura'),
                output_field=models.IntegerField())
        )
        queryset = queryset.annotate(
            ate_vinte=Case(
                When(
                    Q(dias_abertura__gte=0) & Q(dias_abertura__lt=20),
                    then=Value(1)),
                default=Value(0), output_field=models.IntegerField()
            ),
            vinte_trinta=Case(
                When(
                    Q(dias_abertura__gte=20) & Q(dias_abertura__lte=30),
                    then=Value(1)),
                default=Value(0), output_field=models.IntegerField()
            ),
            trinta_mais=Case(
                When(
                    dias_abertura__gt=30,
                    then=Value(1)),
                default=Value(0), output_field=models.IntegerField()
            )
        )
        return queryset.aggregate(
            soma_ate_vinte=Sum('ate_vinte'),
            soma_vinte_trinta=Sum('vinte_trinta'),
            soma_trinta_mais=Sum('trinta_mais')
        )


class InvestigacoesManager(models.Manager):
    def em_curso(self, orgao_id, regras):
        return self.get_queryset().filter(
            docu_orgi_orga_dk_responsavel=orgao_id,
            docu_cldc_dk__in=regras,
            docu_fsdc_dk=1
        )


class ProcessosManager(InvestigacoesManager):
    def em_juizo(self, orgao_id, regras):
        return super().em_curso(orgao_id, regras)


class FinalizadosManager(models.Manager):
    def no_orgao(self, orgao_id, regras_saidas):
        return self.get_queryset().filter(
            andamento__vista__documento__docu_orgi_orga_dk_responsavel=orgao_id,
            stao_tppr_dk__in=regras_saidas
        )

    def trinta_dias(self, orgao_id, regras_saidas):
        finalizados = self.no_orgao(orgao_id, regras_saidas)
        return finalizados.filter(
            andamento__pcao_dt_andamento__gte=date.today()
            - timedelta(days=30))

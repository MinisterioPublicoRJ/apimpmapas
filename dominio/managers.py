from datetime import date

from django.db import models
from django.db.models import (
    Case,
    Q,
    F,
    ExpressionWrapper,
    Value,
    Sum,
    When,
)
from django.db.models.functions import Substr


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

    def abertas_por_data(self, orgao_id, cpf):
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
        return queryset

    def agg_abertas_por_data(self, orgao_id, cpf):
        return self.abertas_por_data(orgao_id, cpf).aggregate(
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
        """
        Para um documento estar em Juízo este precisa de um número do TJRJ.
        Para tal, o número 819 deve estar presente entre as posicoes 14⁻17
        e a string entre as posicoes 10-14 deve ser igual ao campo DOCU_ANO
        """

        docs_tj = super().em_curso(orgao_id, regras)
        docs_tj = docs_tj.annotate(
            nr_ano=Substr("docu_nr_externo", 10, 4),
            codigo_tj=Substr("docu_nr_externo", 14, 3)
        )
        return docs_tj.filter(nr_ano=F("docu_ano"), codigo_tj="819")

from datetime import date, timedelta

from django.db import connections, models
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
            orgao=orgao_id,
            responsavel__cpf=cpf
        )

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

    def aberturas_30_dias_PIP(self, orgao_id, cpf):
        # cldc_dk 590 = PIC, 3 e 494 = Inquerito Policial
        return self.get_queryset().filter(
            Q(data_abertura__gte=date.today() - timedelta(days=30)),
            Q(data_abertura__lte=date.today()),
            Q(documento__docu_cldc_dk__in=[3, 494, 590]),
            orgao=orgao_id,
            responsavel__cpf=cpf
        )


class InvestigacoesManager(models.Manager):
    def em_curso(self, orgao_id, regras):
        parametros = ",".join([f":regra{i}" for i in range(len(regras))])
        query = f"""
            SELECT COUNT(DOCU_FSDC_DK) AS "__COUNT" FROM "MCPR_DOCUMENTO"
            WHERE ("MCPR_DOCUMENTO"."DOCU_CLDC_DK" IN ({parametros})
              AND "MCPR_DOCUMENTO"."DOCU_FSDC_DK" = 1
              AND "MCPR_DOCUMENTO"."DOCU_ORGI_ORGA_DK_RESPONSAVEL" = :orgao_id
              AND NOT ("MCPR_DOCUMENTO"."DOCU_TPST_DK" = 11))
        """
        rs = [(0,)]
        prep_stat = {f"regra{i}": v for i, v in enumerate(regras)}
        prep_stat["orgao_id"] = orgao_id
        with connections["dominio_db"].cursor() as cursor:
            cursor.execute(query, prep_stat)
            rs = cursor.fetchall()

        return rs[0][0]

    def em_curso_pip_aisp(self, orgao_ids):
        return self.get_queryset().filter(
            docu_orgi_orga_dk_responsavel__in=orgao_ids,
            docu_cldc_dk__in=[3, 494, 590],
            docu_fsdc_dk=1
        ).exclude(docu_tpst_dk=11)

    def em_curso_grupo(self, orgao_ids, regras):
        parametros = ",".join([f":regra{i}" for i in range(len(regras))])
        orgaos = ",".join([f":orgao{i}" for i in range(len(orgao_ids))])
        query = f"""
            SELECT /*+ PARALLEL,2 */ COUNT(DOCU_FSDC_DK) AS "__COUNT" FROM "MCPR_DOCUMENTO"
            WHERE ("MCPR_DOCUMENTO"."DOCU_CLDC_DK" IN ({parametros})
             AND "MCPR_DOCUMENTO"."DOCU_FSDC_DK" = 1
             AND "MCPR_DOCUMENTO"."DOCU_ORGI_ORGA_DK_RESPONSAVEL" IN ({orgaos})
             AND NOT ("MCPR_DOCUMENTO"."DOCU_TPST_DK" = 11))
        """
        rs = [(0,)]
        prep_stat = {f"regra{i}": v for i, v in enumerate(regras)}
        prep_stat.update({f"orgao{i}": v for i, v in enumerate(orgao_ids)})
        with connections["dominio_db"].cursor() as cursor:
            cursor.execute(query, prep_stat)
            rs = cursor.fetchall()

        return rs[0][0]


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


class FinalizadosManager(models.Manager):
    def no_orgao(self, org_id, regras_saidas):
        # docu_tpst_dk = 11 : documentos cancelados (desconsiderados)
        # pcao_dt_cancelamento = null : andamentos valido
        return self.get_queryset().filter(
            andamento__vista__documento__docu_orgi_orga_dk_responsavel=org_id,
            stao_tppr_dk__in=regras_saidas,
            andamento__pcao_dt_cancelamento__isnull=True
        ).exclude(andamento__vista__documento__docu_tpst_dk=11)

    def trinta_dias(self, orgao_id, regras, regras_desarq=None):
        finalizados = self.no_orgao(orgao_id, regras)
        finalizados = finalizados.filter(
            andamento__pcao_dt_andamento__gte=date.today()
            - timedelta(days=30))

        # A implementação dos desarquivamentos impactou muito a performance
        # Como são poucos os casos de desarquivamento, foi decidido deixar
        # o cálculo como está, sem considerá-los

        # desarquivamentos = finalizados.filter(stao_tppr_dk__in=regras_desarq)
        # if desarquivamentos.exists():
        #     q_statement = Q()
        #     for record in desarquivamentos:
        #         docu_dk_desarq =\
        #           record['andamento__vista__documento__docu_dk']
        #         dt_desarq = record['andamento__pcao_dt_andamento']
        #         q_statement |= (
        #             Q(andamento__vista__documento__docu_dk__exact=\
        #               docu_dk_desarq) &
        #             Q(andamento__pcao_dt_andamento__lte=dt_desarq)
        #             )
        #     finalizados = finalizados.exclude(q_statement)

        return finalizados\
            .values('andamento__vista__documento__docu_dk').distinct()

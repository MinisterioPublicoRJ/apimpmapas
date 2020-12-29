from datetime import date, timedelta

from django.conf import settings
from django.core.cache import cache
from django.db import connections, models
from django.db.models import (
    Case,
    Q,
    F,
    ExpressionWrapper,
    Value,
    When,
)


class VistaManager(models.Manager):
    def __filter_inactive(self, qs, orgao_id):
        # Import em escopo interno para evitar erros de loop de import
        from dominio.suamesa.dao import DocumentosArquivadosDAO
        docs_arquivados = set(DocumentosArquivadosDAO.get(orgao_id=orgao_id))

        return [x for x in qs if x['docu_dk'] not in docs_arquivados]

    def __abertas_base(self):
        TUTELA_INVESTIGACOES = [51219, 51220, 51221, 51222, 51223, 392, 395]
        return self.get_queryset().filter(
            Q(data_fechamento=None) |
            Q(data_fechamento__gt=date.today())
        ).exclude(
            Q(documento__docu_tpst_dk=3) &
            Q(documento__docu_cldc_dk__in=TUTELA_INVESTIGACOES)
        )

    def __abertas_promotor_base(self, orgao_id, cpf):
        """Busca o número de vistas abertas para um dado órgão e matrícula
        na base do Oracle.

        Arguments:
            orgao_id {integer} -- ID do órgão a ser procurado.
            cpf {String} -- cpf do usuário detentor das vistas.

        Returns:
            List[Tuple] -- Lista com o resultado da query.
        """
        return self.__abertas_base().filter(
            orgao=orgao_id,
            responsavel__cpf=cpf,
        )

    def __abertas_por_data_base(self, orgao_id, cpf):
        """
        Busca o número de vistas abertas para um um dado órgão e matrícula
        agrupadas com a contagem de dias que estão abertas

        Arguments:
            orgao_id {integer} -- ID do órgão a ser procurado.
            cpf {String} -- cpf do usuário detentor das vistas.
        """

        queryset = self.__abertas_promotor_base(orgao_id, cpf).annotate(
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

    def __abertas_lista_filtrada(self, orgao_id, cpf):
        cache_key = 'VISTAMANAGER_DATA_{}_{}'.format(orgao_id, cpf)
        data = cache.get(cache_key, default=None)
        if not data:
            queryset = self.__abertas_por_data_base(orgao_id, cpf)\
                .order_by('-data_abertura')\
                .values(
                    numero_mprj=F("documento__docu_nr_mp"),
                    numero_externo=F("documento__docu_nr_externo"),
                    dt_abertura=F("data_abertura"),
                    classe=F("documento__classe__descricao"),
                    docu_dk=F("documento__docu_dk"),
                    ate_vinte=F("ate_vinte"),
                    vinte_trinta=F("vinte_trinta"),
                    trinta_mais=F("trinta_mais")
                )
            data = self.__filter_inactive(queryset, orgao_id)
            cache.set(cache_key, data, timeout=settings.CACHE_TIMEOUT)
        return data

    def abertas_promotor(self, orgao_id, cpf):
        return len(self.__abertas_lista_filtrada(orgao_id, cpf))

    def abertas_por_data(self, orgao_id, cpf, abertura):
        return self.__abertas_lista_filtrada(orgao_id, cpf)

    def agg_abertas_por_data(self, orgao_id, cpf):
        data = self.__abertas_lista_filtrada(orgao_id, cpf)

        s1, s2, s3 = 0, 0, 0
        for x in data:
            s1 += x['ate_vinte']
            s2 += x['vinte_trinta']
            s3 += x['trinta_mais']

        return {
            'soma_ate_vinte': s1,
            'soma_vinte_trinta': s2,
            'soma_trinta_mais': s3
        }


class InvestigacoesManager(models.Manager):
    def em_curso(self, orgao_id, regras, remove_out=False):
        parametros = ",".join([f":regra{i}" for i in range(len(regras))])
        query = f"""
            SELECT docu_dk FROM "MCPR_DOCUMENTO"
            WHERE ("MCPR_DOCUMENTO"."DOCU_CLDC_DK" IN ({parametros})
              AND "MCPR_DOCUMENTO"."DOCU_FSDC_DK" = 1
              AND "MCPR_DOCUMENTO"."DOCU_ORGI_ORGA_DK_RESPONSAVEL" = :orgao_id
              AND NOT ("MCPR_DOCUMENTO"."DOCU_TPST_DK" = 11))
        """
        if remove_out:
            query += """ AND NOT ("MCPR_DOCUMENTO"."DOCU_TPST_DK" = 3)"""
        rs = [(0,)]
        prep_stat = {f"regra{i}": v for i, v in enumerate(regras)}
        prep_stat["orgao_id"] = orgao_id
        with connections["dominio_db"].cursor() as cursor:
            cursor.execute(query, prep_stat)
            rs = cursor.fetchall()

        from dominio.suamesa.dao import DocumentosArquivadosDAO
        docs_arquivados = DocumentosArquivadosDAO.get(orgao_id=orgao_id)

        return len([r[0] for r in rs if r[0] not in docs_arquivados])

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
            SELECT /*+ PARALLEL,2 */
            docu_dk FROM "MCPR_DOCUMENTO"
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

        from dominio.suamesa.dao import DocumentosArquivadosMultiplosOrgaosDAO
        docs_arquivados = DocumentosArquivadosMultiplosOrgaosDAO.get(
            ids_orgaos=orgao_ids
        )

        return len([r[0] for r in rs if r[0] not in docs_arquivados])


class ProcessosManager(InvestigacoesManager):
    def em_juizo(self, orgao_id, regras):
        """
        Para um documento estar em Juízo este precisa de um número do TJRJ.
        Para tal, o número 819 deve estar presente entre as posicoes 14⁻17
        e a string entre as posicoes 10-14 deve ser igual ao campo DOCU_ANO
        """
        parametros = ",".join([f":regra{i}" for i in range(len(regras))])
        query = f"""
            SELECT docu_dk FROM "MCPR_DOCUMENTO"
            WHERE ("MCPR_DOCUMENTO"."DOCU_CLDC_DK" IN ({parametros})
              AND "MCPR_DOCUMENTO"."DOCU_FSDC_DK" = 1
              AND "MCPR_DOCUMENTO"."DOCU_ORGI_ORGA_DK_RESPONSAVEL" = :orgao_id
              AND NOT ("MCPR_DOCUMENTO"."DOCU_TPST_DK" = 11)
              AND SUBSTR("MCPR_DOCUMENTO"."DOCU_NR_EXTERNO", 10, 4)
                = "MCPR_DOCUMENTO"."DOCU_ANO"
              AND SUBSTR("MCPR_DOCUMENTO"."DOCU_NR_EXTERNO", 14, 3) = '819')
        """
        rs = [(0,)]
        prep_stat = {f"regra{i}": v for i, v in enumerate(regras)}
        prep_stat["orgao_id"] = orgao_id
        with connections["dominio_db"].cursor() as cursor:
            cursor.execute(query, prep_stat)
            rs = cursor.fetchall()

        from dominio.suamesa.dao import DocumentosArquivadosDAO
        docs_arquivados = DocumentosArquivadosDAO.get(orgao_id=orgao_id)

        return len([r[0] for r in rs if r[0] not in docs_arquivados])


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

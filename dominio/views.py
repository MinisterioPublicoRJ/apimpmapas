from datetime import datetime, timedelta

from django.conf import settings
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.http import Http404
from rest_framework.response import Response
from rest_framework.views import APIView

from dominio import suamesa
from .db_connectors import run_query
from .models import Vista, Documento, SubAndamento
from .serializers import (
    SaidasSerializer,
    OutliersSerializer,
    EntradasSerializer,
    DetalheAcervoSerializer,
    DetalheProcessosJuizoSerializer
)


@method_decorator(
    cache_page(
        settings.CACHE_TIMEOUT,
        key_prefix="dominio_acervo_variation_topn"),
    name="dispatch"
)
class DetalheAcervoView(APIView):

    @staticmethod
    def get_variacao_orgao(l, orgao_id):
        for element in l:
            # orgao_id comes in position 0 of each element
            if element[0] == orgao_id:
                return element[4]
        return None

    @staticmethod
    def get_top_n_orgaos(l, n=3):
        sorted_list = sorted(l, key=lambda el: float(el[4]), reverse=True)
        result_list = [
            {'nm_promotoria': el[1], 'variacao_acervo': el[4]}
            for el in sorted_list
        ]
        return result_list[:n]

    @staticmethod
    def get_acervo_increase(orgao_id, dt_inicio, dt_fim):
        query = """
                WITH tb_acervo_orgao_pct as (
                    SELECT *
                    FROM {namespace}.tb_acervo ac
                    INNER JOIN (
                        SELECT cod_pct, orgi_nm_orgao as nm_orgao
                        FROM {namespace}.atualizacao_pj_pacote
                        WHERE id_orgao = :orgao_id
                        ) org
                    ON org.cod_pct = ac.cod_atribuicao)
                SELECT
                    tb_data_fim.cod_orgao,
                    tb_data_fim.nm_orgao,
                    tb_data_fim.acervo_fim,
                    tb_data_inicio.acervo_inicio,
                    (acervo_fim - acervo_inicio)/acervo_inicio as variacao
                FROM (
                    SELECT cod_orgao, nm_orgao, SUM(acervo) as acervo_fim
                    FROM tb_acervo_orgao_pct acpc
                    INNER JOIN {namespace}.tb_regra_negocio_investigacao regras
                        ON regras.cod_atribuicao = acpc.cod_atribuicao
                        AND regras.classe_documento = acpc.tipo_acervo
                    WHERE dt_inclusao = to_timestamp(:dt_fim, 'yyyy-MM-dd')
                    GROUP BY cod_orgao, nm_orgao
                    ) tb_data_fim
                INNER JOIN (
                    SELECT cod_orgao, nm_orgao, SUM(acervo) as acervo_inicio
                    FROM tb_acervo_orgao_pct acpc
                    INNER JOIN {namespace}.tb_regra_negocio_investigacao regras
                        ON regras.cod_atribuicao = acpc.cod_atribuicao
                        AND regras.classe_documento = acpc.tipo_acervo
                    WHERE dt_inclusao = to_timestamp(:dt_inicio, 'yyyy-MM-dd')
                    GROUP BY cod_orgao, nm_orgao
                    ) tb_data_inicio
                ON tb_data_fim.cod_orgao = tb_data_inicio.cod_orgao
                """.format(namespace=settings.TABLE_NAMESPACE)
        parameters = {
            'orgao_id': orgao_id,
            'dt_inicio': dt_inicio,
            'dt_fim': dt_fim
        }
        print(parameters)
        return run_query(query, parameters)

    def get(self, request, *args, **kwargs):
        orgao_id = int(self.kwargs['orgao_id'])

        date_today = datetime.now().date()
        dt_fim = str(date_today)
        dt_inicio = date_today - timedelta(30)
        dt_inicio = '2020-02-10' if datetime(2020, 2, 10).date() > dt_inicio \
            else str(dt_inicio)
        n = 3

        data = self.get_acervo_increase(
            orgao_id=orgao_id,
            dt_inicio=dt_inicio,
            dt_fim=dt_fim
        )

        if not data:
            raise Http404

        variacao_acervo = self.get_variacao_orgao(data, orgao_id)
        top_n = self.get_top_n_orgaos(data, n=n)

        data_obj = {
            'variacao_acervo': variacao_acervo,
            'top_n': top_n
        }

        data = DetalheAcervoSerializer(data_obj).data
        return Response(data)


@method_decorator(
    cache_page(300, key_prefix="dominio_outliers"),
    name="dispatch"
)
class OutliersView(APIView):

    def get_acervo(self, orgao_id, data):
        query = (
            "SELECT SUM(acervo) "
            "FROM {namespace}.tb_acervo A "
            "INNER JOIN cluster.atualizacao_pj_pacote B "
            "ON A.cod_orgao = cast(B.id_orgao as int) "
            "INNER JOIN {namespace}.tb_regra_negocio_investigacao C "
            "ON C.cod_atribuicao = B.cod_pct "
            "AND C.classe_documento = A.tipo_acervo "
            "WHERE cod_orgao = :orgao_id "
            "AND dt_inclusao = to_timestamp(:data, 'yyyy-MM-dd')"
            .format(
                namespace=settings.TABLE_NAMESPACE
            ))
        parameters = {
            'orgao_id': orgao_id,
            'data': data
        }
        return run_query(query, parameters)

    def get_outliers(self, orgao_id, dt_calculo):

        query = """
                SELECT B.cod_atribuicao,
                B.minimo,
                B.maximo,
                B.media,
                B.primeiro_quartil,
                B.mediana,
                B.terceiro_quartil,
                B.iqr,
                B.lout,
                B.hout
                FROM {namespace}.tb_acervo A
                INNER JOIN {namespace}.tb_distribuicao B
                ON A.cod_atribuicao = B.cod_atribuicao
                AND A.dt_inclusao = B.dt_inclusao
                WHERE A.cod_orgao = :orgao_id
                AND B.dt_inclusao = to_timestamp(:dt_calculo, 'yyyy-MM-dd')
                """.format(
                    namespace=settings.TABLE_NAMESPACE
                )
        parameters = {
            'orgao_id': orgao_id,
            'dt_calculo': dt_calculo
        }
        return run_query(query, parameters)

    def get(self, request, *args, **kwargs):
        orgao_id = int(self.kwargs['orgao_id'])
        dt_calculo = str(self.kwargs['dt_calculo'])

        data = self.get_outliers(
            orgao_id=orgao_id,
            dt_calculo=dt_calculo
        )
        acervo_qtd = self.get_acervo(
            orgao_id=orgao_id,
            data=dt_calculo
        )

        if not data or not acervo_qtd:
            raise Http404

        fields = ['cod_atribuicao', 'minimo', 'maximo',
                  'media', 'primeiro_quartil', 'mediana', 'terceiro_quartil',
                  'iqr', 'lout', 'hout']
        data_obj = {
            fieldname: value for fieldname, value in zip(fields, data[0])
        }
        data_obj['acervo_qtd'] = acervo_qtd[0][0]
        data = OutliersSerializer(data_obj).data
        return Response(data)


@method_decorator(
    cache_page(300, key_prefix="dominio_saidas"),
    name="dispatch"
)
class SaidasView(APIView):

    def get_saidas(self, orgao_id):

        query = """
                SELECT saidas, id_orgao, cod_pct, percent_rank, dt_calculo
                FROM {namespace}.tb_saida
                WHERE id_orgao = :orgao_id
                """.format(
                    namespace=settings.TABLE_NAMESPACE
                )
        parameters = {
            'orgao_id': orgao_id
        }

        return run_query(query, parameters)

    def get(self, request, *args, **kwargs):
        orgao_id = int(self.kwargs['orgao_id'])

        data = self.get_saidas(
            orgao_id=orgao_id
        )

        if not data:
            raise Http404

        fields = [
            'saidas',
            'id_orgao',
            'cod_pct',
            'percent_rank',
            'dt_calculo'
        ]
        data_obj = {
            fieldname: value for fieldname, value in zip(fields, data[0])
        }
        data = SaidasSerializer(data_obj).data
        return Response(data)


@method_decorator(
    cache_page(300, key_prefix="dominio_entradas"),
    name="dispatch"
)
class EntradasView(APIView):

    def get_entradas(self, orgao_id, nr_cpf):

        query = """
                SELECT
                    nr_entradas_hoje,
                    minimo,
                    maximo,
                    media,
                    primeiro_quartil,
                    mediana,
                    terceiro_quartil,
                    iqr,
                    lout,
                    hout
                FROM {namespace}.tb_dist_entradas
                WHERE comb_orga_dk = :orgao_id
                AND comb_cpf = :nr_cpf
                """.format(
                    namespace=settings.TABLE_NAMESPACE
                )
        parameters = {
            'orgao_id': orgao_id,
            'nr_cpf': nr_cpf
        }

        return run_query(query, parameters)

    def get(self, request, *args, **kwargs):
        orgao_id = int(self.kwargs['orgao_id'])
        nr_cpf = str(self.kwargs['nr_cpf'])

        data = self.get_entradas(
            orgao_id=orgao_id,
            nr_cpf=nr_cpf
        )

        if not data:
            raise Http404

        fields = [
            'nr_entradas_hoje',
            'minimo',
            'maximo',
            'media',
            'primeiro_quartil',
            'mediana',
            'terceiro_quartil',
            'iqr',
            'lout',
            'hout'
        ]
        data_obj = {
            fieldname: value for fieldname, value in zip(fields, data[0])
        }
        data = EntradasSerializer(data_obj).data
        return Response(data)


@method_decorator(
    cache_page(
        settings.CACHE_TIMEOUT,
        key_prefix="dominio_suamesa_vistas"),
    name="dispatch"
)
class SuaMesaVistasAbertas(APIView):
    def get(self, request, *args, **kwargs):
        orgao_id = int(kwargs.get("orgao_id"))
        cpf = kwargs.get("cpf")

        doc_count = Vista.vistas.abertas_promotor(orgao_id, cpf).count()

        return Response(data={"suamesa_vistas": doc_count})


class SuaMesaInvestigacoes(APIView):
    def get(self, request, *args, **kwargs):
        orgao_id = int(kwargs.get("orgao_id"))

        regras_investigacoes = suamesa.get_regras(
            orgao_id,
            tipo='investigacao'
        )
        doc_count = Documento.investigacoes.em_curso(
            orgao_id, regras_investigacoes).count()

        return Response(data={"suamesa_investigacoes": doc_count})


class SuaMesaProcessos(APIView):
    def get(self, request, *args, **kwargs):
        orgao_id = int(kwargs.get("orgao_id"))

        regras_processos = suamesa.get_regras(orgao_id, tipo='processo')
        doc_count = Documento.processos.em_juizo(
            orgao_id, regras_processos).count()

        return Response(data={"suamesa_processos": doc_count})


@method_decorator(
    cache_page(
        settings.CACHE_TIMEOUT,
        key_prefix="dominio_suamesa_finalizados"),
    name="dispatch"
)
class SuaMesaFinalizados(APIView):
    def get(self, request, *args, **kwargs):
        orgao_id = int(kwargs.get("orgao_id"))

        regras_saidas = (6251, 6657, 6655, 6644, 6326)
        doc_count = SubAndamento.finalizados.trinta_dias(
            orgao_id, regras_saidas).count()

        return Response(data={"suamesa_finalizados": doc_count})


class SuaMesaDetalheView(APIView):
    def get(self, request, *args, **kwargs):
        orgao_id = int(kwargs.get("orgao_id"))
        cpf = kwargs.get("cpf")

        mesa_detalhe = Vista.vistas.abertas_por_dias_abertura(orgao_id, cpf)
        if all([v is None for v in mesa_detalhe.values()]):
            raise Http404

        return Response(mesa_detalhe)


@method_decorator(
    cache_page(settings.CACHE_TIMEOUT, key_prefix="dominio_detalhe_processos"),
    name="dispatch"
)
class DetalheProcessosJuizoView(APIView):

    @staticmethod
    def get_numero_acoes_propostas_pacote_atribuicao(orgao_id):
        query = """
            SELECT
                orgao_id,
                nm_orgao,
                nr_acoes_ultimos_60_dias,
                variacao_12_meses,
                nr_acoes_ultimos_30_dias
            FROM {namespace}.tb_detalhe_processo t1
            JOIN (
                SELECT cod_pct
                FROM {namespace}.tb_detalhe_processo
                WHERE orgao_id = :orgao_id) t2
              ON t1.cod_pct = t2.cod_pct
        """.format(namespace=settings.TABLE_NAMESPACE)
        parameters = {
            'orgao_id': orgao_id
        }
        return run_query(query, parameters)

    @staticmethod
    def get_value_from_orgao(l, orgao_id, value_position=2):
        for element in l:
            # orgao_id comes in position 0 of each element
            if element[0] == orgao_id:
                return element[value_position]
        return None

    @staticmethod
    def get_top_n_orgaos(l, n=3):
        sorted_list = sorted(l, key=lambda el: el[4], reverse=True)
        result_list = [
            {'nm_promotoria': el[1], 'nr_acoes_propostas_30_dias': el[4]}
            for el in sorted_list
        ]
        return result_list[:n]

    def get(self, request, *args, **kwargs):
        orgao_id = int(self.kwargs['orgao_id'])

        data_acoes = self.get_numero_acoes_propostas_pacote_atribuicao(
            orgao_id=orgao_id
        )

        if not data_acoes:
            raise Http404

        nr_acoes_60_dias = self.get_value_from_orgao(
            data_acoes, orgao_id, value_position=2)
        variacao_acoes_12_meses = self.get_value_from_orgao(
            data_acoes, orgao_id, value_position=3)
        top_n = self.get_top_n_orgaos(data_acoes, n=3)

        data_obj = {
            'nr_acoes_propostas_60_dias': nr_acoes_60_dias,
            'variacao_12_meses': variacao_acoes_12_meses,
            'top_n': top_n
        }

        data = DetalheProcessosJuizoSerializer(data_obj).data
        return Response(data)


class SuaMesaVistasListaView(APIView):
    def get(self, request, *args, **kwargs):
        return Response()

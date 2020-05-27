from datetime import datetime, timedelta

from django.conf import settings
from django.db import connections
from django.db.models import F
from django.http import Http404
from rest_framework.response import Response
from rest_framework.views import APIView


from dominio.tutela import suamesa
from dominio.db_connectors import run_query
from dominio.mixins import CacheMixin, PaginatorMixin, JWTAuthMixin
from dominio.models import Vista, Documento, SubAndamento
from dominio.tutela.serializers import (
    SaidasSerializer,
    OutliersSerializer,
    EntradasSerializer,
    DetalheAcervoSerializer,
    DetalheProcessosJuizoSerializer,
    SuaMesaListaVistasSerializer,
)
from dominio.utils import (
    get_value_given_key,
    get_top_n_orderby_value_as_dict
)
from dominio.tutela.dao import TempoTramitacaoIntegradoDAO, TempoTramitacaoDAO


class DetalheAcervoView(JWTAuthMixin, CacheMixin, APIView):
    cache_config = 'DETALHE_ACERVO_CACHE_TIMEOUT'

    @staticmethod
    def get_acervo_increase(orgao_id, dt_inicio, dt_fim):
        query = """
                WITH tb_acervo_orgao_pct as (
                    SELECT *
                    FROM {namespace}.tb_acervo ac
                    INNER JOIN (
                        SELECT cod_pct
                        FROM {namespace}.atualizacao_pj_pacote
                        WHERE id_orgao = :orgao_id
                        ) org
                    ON org.cod_pct = ac.cod_atribuicao)
                SELECT
                    tb_data_fim.cod_orgao,
                    pc.orgi_nm_orgao as nm_orgao,
                    tb_data_fim.acervo_fim,
                    tb_data_inicio.acervo_inicio,
                    (acervo_fim - acervo_inicio)/acervo_inicio as variacao
                FROM (
                    SELECT cod_orgao, SUM(acervo) as acervo_fim
                    FROM tb_acervo_orgao_pct acpc
                    INNER JOIN {namespace}.tb_regra_negocio_investigacao regras
                        ON regras.cod_atribuicao = acpc.cod_atribuicao
                        AND regras.classe_documento = acpc.tipo_acervo
                    WHERE dt_inclusao = to_timestamp(:dt_fim, 'yyyy-MM-dd')
                    GROUP BY cod_orgao
                    ) tb_data_fim
                INNER JOIN (
                    SELECT cod_orgao, SUM(acervo) as acervo_inicio
                    FROM tb_acervo_orgao_pct acpc
                    INNER JOIN {namespace}.tb_regra_negocio_investigacao regras
                        ON regras.cod_atribuicao = acpc.cod_atribuicao
                        AND regras.classe_documento = acpc.tipo_acervo
                    WHERE dt_inclusao = to_timestamp(:dt_inicio, 'yyyy-MM-dd')
                    GROUP BY cod_orgao
                    ) tb_data_inicio
                ON tb_data_fim.cod_orgao = tb_data_inicio.cod_orgao
                INNER JOIN {namespace}.atualizacao_pj_pacote pc
                ON pc.id_orgao = tb_data_fim.cod_orgao
                """.format(namespace=settings.TABLE_NAMESPACE)
        parameters = {
            'orgao_id': orgao_id,
            'dt_inicio': dt_inicio,
            'dt_fim': dt_fim
        }

        return run_query(query, parameters)

    def get(self, request, *args, **kwargs):
        orgao_id = int(self.kwargs['orgao_id'])

        date_today = datetime.now().date()
        dt_fim = str(date_today)
        dt_inicio = str(date_today - timedelta(30))

        data = self.get_acervo_increase(
            orgao_id=orgao_id,
            dt_inicio=dt_inicio,
            dt_fim=dt_fim
        )

        if not data:
            raise Http404

        variacao_acervo = get_value_given_key(
            data, orgao_id, key_position=0, value_position=4)
        top_n = get_top_n_orderby_value_as_dict(
            data,
            name_position=1,
            value_position=4,
            name_fieldname='nm_promotoria',
            value_fieldname='variacao_acervo',
            n=3)

        data_obj = {
            'variacao_acervo': variacao_acervo,
            'top_n': top_n
        }

        data = DetalheAcervoSerializer(data_obj).data
        return Response(data)


class OutliersView(JWTAuthMixin, CacheMixin, APIView):
    cache_config = 'OUTLIERS_CACHE_TIMEOUT'
    _fields = [
        'cod_orgao',
        'acervo_qtd',
        'cod_atribuicao',
        'minimo',
        'maximo',
        'media',
        'primeiro_quartil',
        'mediana',
        'terceiro_quartil',
        'iqr',
        'lout',
        'hout',
        'dt_inclusao',
    ]

    def get_data(self, orgao_id):
        query = """
                SELECT
                cod_orgao,
                acervo,
                cod_atribuicao,
                minimo,
                maximo,
                media,
                primeiro_quartil,
                mediana,
                terceiro_quartil,
                iqr,
                lout,
                hout,
                dt_inclusao
                FROM {namespace}.tb_distribuicao
                WHERE cod_orgao = :orgao_id
                """.format(
                    namespace=settings.TABLE_NAMESPACE
                )
        parameters = {
            'orgao_id': orgao_id
        }
        return run_query(query, parameters)

    def get(self, request, *args, **kwargs):
        orgao_id = int(self.kwargs['orgao_id'])

        data = self.get_data(
            orgao_id=orgao_id
        )

        if not data:
            raise Http404

        data_obj = dict(zip(self._fields, data[0]))

        data = OutliersSerializer(data_obj).data
        return Response(data)


class SaidasView(JWTAuthMixin, CacheMixin, APIView):
    cache_config = 'SAIDAS_CACHE_TIMEOUT'

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


class EntradasView(JWTAuthMixin, CacheMixin, APIView):
    cache_config = 'ENTRADAS_CACHE_TIMEOUT'

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


class SuaMesaVistasAbertas(JWTAuthMixin, CacheMixin, APIView):
    cache_config = 'SUAMESAVISTAS_CACHE_TIMEOUT'

    def get(self, request, *args, **kwargs):
        orgao_id = int(kwargs.get("orgao_id"))
        cpf = kwargs.get("cpf")

        doc_count = Vista.vistas.abertas_promotor(orgao_id, cpf).count()

        return Response(data={"suamesa_vistas": doc_count})


class SuaMesaInvestigacoes(JWTAuthMixin, CacheMixin, APIView):
    cache_config = 'SUAMESAINVESTIGACOES_CACHE_TIMEOUT'

    def get(self, request, *args, **kwargs):
        orgao_id = int(kwargs.get("orgao_id"))

        regras_investigacoes = suamesa.get_regras(
            orgao_id,
            tipo='investigacao'
        )
        doc_count = Documento.investigacoes.em_curso(
            orgao_id, regras_investigacoes).count()

        return Response(data={"suamesa_investigacoes": doc_count})


class SuaMesaProcessos(JWTAuthMixin, CacheMixin, APIView):
    cache_config = 'SUAMESAPROCESSOS_CACHE_TIMEOUT'

    def get(self, request, *args, **kwargs):
        orgao_id = int(kwargs.get("orgao_id"))

        regras_processos = suamesa.get_regras(orgao_id, tipo='processo')
        doc_count = Documento.processos.em_juizo(
            orgao_id, regras_processos).count()

        return Response(data={"suamesa_processos": doc_count})


class SuaMesaFinalizados(JWTAuthMixin, CacheMixin, APIView):
    cache_config = 'SUAMESAFINALIZADOS_CACHE_TIMEOUT'

    def get(self, request, *args, **kwargs):
        orgao_id = int(kwargs.get("orgao_id"))

        regras_saidas = (6251, 6657, 6655, 6644, 6326)
        regras_arquiv = (7912, 6548, 6326, 6681, 6678, 6645, 6682, 6680, 6679,
                         6644, 6668, 6666, 6665, 6669, 6667, 6664, 6655, 6662,
                         6659, 6658, 6663, 6661, 6660, 6657, 6670, 6676, 6674,
                         6673, 6677, 6675, 6672, 6018, 6341, 6338, 6019, 6017,
                         6591, 6339, 6553, 7871, 6343, 6340, 6342, 6021, 6334,
                         6331, 6022, 6020, 6593, 6332, 7872, 6336, 6333, 6335,
                         7745, 6346, 6345, 6015, 6016, 6325, 6327, 6328, 6329,
                         6330, 6337, 6344, 6656, 6671, 7869, 7870, 6324)

        regras_finalizacoes = regras_saidas + regras_arquiv
        doc_count = SubAndamento.finalizados.trinta_dias(
            orgao_id, regras_finalizacoes)\
            .values('andamento__vista__documento__docu_dk')\
            .distinct()\
            .count()

        return Response(data={"suamesa_finalizados": doc_count})


class SuaMesaDetalheView(JWTAuthMixin, CacheMixin, APIView):
    cache_config = 'SUAMESADETALHE_CACHE_TIMEOUT'

    def get(self, request, *args, **kwargs):
        orgao_id = int(kwargs.get("orgao_id"))
        cpf = kwargs.get("cpf")

        mesa_detalhe = Vista.vistas.agg_abertas_por_data(orgao_id, cpf)
        if all([v is None for v in mesa_detalhe.values()]):
            raise Http404

        return Response(mesa_detalhe)


class DetalheProcessosJuizoView(JWTAuthMixin, CacheMixin, APIView):
    cache_config = 'DETALHEPROCESSO_CACHE_TIMEOUT'

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

    def get(self, request, *args, **kwargs):
        orgao_id = int(self.kwargs['orgao_id'])

        data_acoes = self.get_numero_acoes_propostas_pacote_atribuicao(
            orgao_id=orgao_id
        )

        if not data_acoes:
            raise Http404

        nr_acoes_60_dias = get_value_given_key(
            data_acoes, orgao_id, key_position=0, value_position=2)
        variacao_acoes_12_meses = get_value_given_key(
            data_acoes, orgao_id, key_position=0, value_position=3)
        top_n = get_top_n_orderby_value_as_dict(
            data_acoes,
            name_position=1,
            value_position=4,
            name_fieldname='nm_promotoria',
            value_fieldname='nr_acoes_propostas_30_dias',
            n=3)

        data_obj = {
            'nr_acoes_propostas_60_dias': nr_acoes_60_dias,
            'variacao_12_meses': variacao_acoes_12_meses,
            'top_n': top_n
        }

        data = DetalheProcessosJuizoSerializer(data_obj).data
        return Response(data)


class SuaMesaVistasListaView(
        JWTAuthMixin, CacheMixin, PaginatorMixin, APIView):
    cache_config = 'SUAMESAVISTASLISTA_CACHE_TIMEOUT'

    def get(self, request, *args, **kwargs):
        orgao_id = int(kwargs.get("orgao_id"))
        cpf = kwargs.get("cpf")
        abertura = kwargs.get("abertura")
        lista_aberturas = ("ate_vinte", "vinte_trinta", "trinta_mais")
        page = int(request.GET.get("page", 1))

        if abertura not in lista_aberturas:
            msg = "data_abertura inválida. "\
                  f"Opções são: {', '.join(lista_aberturas)}"
            return Response(data=msg, status=404)

        data = Vista.vistas.abertas_por_data(orgao_id, cpf).filter(
            **{abertura: 1}
        ).order_by('-data_abertura').values(
            numero_mprj=F("documento__docu_nr_mp"),
            numero_externo=F("documento__docu_nr_externo"),
            dt_abertura=F("data_abertura"),
            classe=F("documento__classe__descricao")
        )
        page_data = self.paginate(
            data,
            page=page,
            page_size=suamesa.VISTAS_PAGE_SIZE
        )

        vistas_lista = SuaMesaListaVistasSerializer(page_data, many=True).data

        return Response(data=vistas_lista)


class TempoTramitacaoView(JWTAuthMixin, CacheMixin, APIView):
    cache_config = 'TEMPO_TRAMITACAO_CACHE_TIMEOUT'

    def get(self, request, *args, **kwargs):
        orgao_id = int(self.kwargs['orgao_id'])
        version = self.request.GET.get('version')

        if version == '1.1':
            DAO = TempoTramitacaoIntegradoDAO
        else:
            DAO = TempoTramitacaoDAO

        data = DAO.get(orgao_id=orgao_id)

        return Response(data)


class DesarquivamentosView(JWTAuthMixin, CacheMixin, APIView):
    cache_config = "DESARQUIVAMENTOS_CACHE_TIMEOUT"
    fields = ["numero_mprj", "qtd_desarq"]

    def fetch_set(self, cursor):
        return [dict(zip(self.fields, row)) for row in cursor.fetchall()]

    def get_data(self, orgao_id):
        with connections["dominio_db"].cursor() as cursor:
            query = """
                WITH AGRUPADOS AS (SELECT d.docu_nr_mp, COUNT(d.docu_nr_mp)
                FROM MCPR_DOCUMENTO d
                JOIN mcpr_vista v ON v.vist_docu_dk = d.docu_dk
                JOIN mcpr_andamento a ON a.pcao_vist_dk = v.vist_dk
                JOIN mcpr_sub_andamento sa ON sa.stao_pcao_dk = a.pcao_dk
                JOIN mcpr_tp_andamento ta ON ta.tppr_dk = sa.stao_tppr_dk
                WHERE sa.stao_tppr_dk IN (6075, 1028, 6798, 7245, 6307, 1027,
                                          7803, 6003, 7802, 7801)
                                          AND d.docu_cldc_dk = 392
                AND d.DOCU_ORGI_ORGA_DK_RESPONSAVEL = %s
                AND d.DOCU_TPST_DK != 11
                AND a.pcao_dt_cancelamento IS NULL
                GROUP BY docu_nr_mp, a.pcao_dt_andamento)
                SELECT docu_nr_mp, COUNT(docu_nr_mp)
                FROM AGRUPADOS GROUP BY docu_nr_mp
            """
            result_set = cursor.execute(query, [orgao_id])
            return self.fetch_set(result_set)

    def get(self, request, *args, **kwargs):
        orgao_id = int(self.kwargs['orgao_id'])
        # TODO: pensar numa forma geral de discernir 404 de respostas
        # vazias e respostas não existentes

        return Response(data=self.get_data(orgao_id))


class ListaProcessosView(JWTAuthMixin, CacheMixin, PaginatorMixin, APIView):
    cache_config = 'LISTA_PROCESSOS_CACHE_TIMEOUT'
    PROCESSOS_SIZE = 20

    def get_data(self, orgao_id):
        query = """
            SELECT * FROM {namespace}.tb_lista_processos
            WHERE orgao_dk = :orgao_id
            ORDER BY dt_ultimo_andamento DESC
        """.format(namespace=settings.TABLE_NAMESPACE)
        parameters = {"orgao_id": orgao_id}

        return run_query(query, parameters)

    def get(self, request, *args, **kwargs):
        orgao_id = int(self.kwargs['orgao_id'])
        page = int(request.GET.get("page", 1))

        data = self.get_data(orgao_id)

        if not data:
            raise Http404

        fields = [
            'id_orgao',
            'classe_documento',
            'docu_nr_mp',
            'docu_nr_externo',
            'docu_etiqueta',
            'docu_personagens',
            'dt_ultimo_andamento',
            'ultimo_andamento',
            'url_tjrj'
        ]
        data_obj = [dict(zip(fields, row)) for row in data]

        page_data = self.paginate(
            data_obj,
            page=page,
            page_size=self.PROCESSOS_SIZE
        )

        return Response(data=page_data)

import ring
from django.conf import settings
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.http import Http404
from rest_framework.response import Response
from rest_framework.views import APIView

from .db_connectors import run_query
from .models import Vista, Documento, SubAndamento
from .serializers import (
    AcervoSerializer,
    SaidasSerializer,
    AcervoVariationSerializer,
    AcervoVariationTopNSerializer,
    OutliersSerializer,
    EntradasSerializer,
)


@method_decorator(
    cache_page(settings.CACHE_TIMEOUT, key_prefix="dominio_acervo"),
    name="dispatch"
)
class AcervoView(APIView):

    def get_acervo(self, orgao_id, data):
        query = (
            "SELECT SUM(acervo) "
            "FROM {namespace}.tb_acervo A "
            "INNER JOIN cluster.atualizacao_pj_pacote B "
            "ON A.cod_orgao = cast(B.id_orgao as int) "
            "INNER JOIN {namespace}.tb_regra_negocio_investigacao C "
            "ON C.cod_atribuicao = B.cod_pct "
            "AND C.classe_documento = A.tipo_acervo "
            "WHERE cod_orgao = {orgao_id} "
            "AND dt_inclusao = to_timestamp('{data}', 'yyyy-MM-dd')"
            .format(
                namespace=settings.TABLE_NAMESPACE,
                orgao_id=orgao_id,
                data=data
            ))
        return run_query(query)

    def get(self, request, *args, **kwargs):
        orgao_id = int(self.kwargs['orgao_id'])
        data = str(self.kwargs['data'])

        acervo_qtd = self.get_acervo(
            orgao_id=orgao_id,
            data=data
        )

        if not acervo_qtd:
            raise Http404

        acervo = {'acervo_qtd': acervo_qtd[0][0]}
        data = AcervoSerializer(acervo).data
        return Response(data)


@method_decorator(
    cache_page(settings.CACHE_TIMEOUT, key_prefix="dominio_acervo_variation"),
    name="dispatch"
)
class AcervoVariationView(APIView):

    def get_acervo_increase(self, orgao_id, dt_inicio, dt_fim):
        query = """
            SELECT
                acervo_fim,
                acervo_inicio,
                (acervo_fim - acervo_inicio)/acervo_inicio as variacao
            FROM (
                SELECT
                    SUM(tb_data_fim.acervo) as acervo_fim,
                    SUM(tb_data_inicio.acervo_inicio) as acervo_inicio
                FROM {namespace}.tb_acervo tb_data_fim
                INNER JOIN (
                    SELECT
                        acervo as acervo_inicio,
                        dt_inclusao as data_inicio,
                        cod_orgao,
                        tipo_acervo
                    FROM {namespace}.tb_acervo
                    WHERE dt_inclusao = to_timestamp(
                        '{dt_inicio}', 'yyyy-MM-dd')
                    ) tb_data_inicio
                ON tb_data_fim.cod_orgao = tb_data_inicio.cod_orgao
                    AND tb_data_fim.tipo_acervo = tb_data_inicio.tipo_acervo
                INNER JOIN {namespace}.tb_regra_negocio_investigacao regras
                ON regras.cod_atribuicao = tb_data_fim.cod_atribuicao
                    AND regras.classe_documento = tb_data_fim.tipo_acervo
                WHERE tb_data_fim.dt_inclusao = to_timestamp(
                    '{dt_fim}', 'yyyy-MM-dd')
                AND tb_data_fim.cod_orgao = {orgao_id}) t
            """.format(
                namespace=settings.TABLE_NAMESPACE,
                orgao_id=orgao_id,
                dt_inicio=dt_inicio,
                dt_fim=dt_fim
            )
        return run_query(query)

    def get(self, request, *args, **kwargs):
        orgao_id = int(self.kwargs['orgao_id'])
        dt_inicio = str(self.kwargs['dt_inicio'])
        dt_fim = str(self.kwargs['dt_fim'])

        data = self.get_acervo_increase(
            orgao_id=orgao_id,
            dt_inicio=dt_inicio,
            dt_fim=dt_fim
        )

        if not data:
            raise Http404

        fields = ['acervo_fim', 'acervo_inicio', 'variacao']
        data_obj = {
            fieldname: value for fieldname, value in zip(fields, data[0])
        }
        data = AcervoVariationSerializer(data_obj).data
        return Response(data)


@method_decorator(
    cache_page(
        settings.CACHE_TIMEOUT,
        key_prefix="dominio_acervo_variation_topn"),
    name="dispatch"
)
class AcervoVariationTopNView(APIView):
    queryset = ''

    def get_acervo_increase_topn(self, orgao_id, dt_inicio, dt_fim, n=3):
        query = """
                SELECT
                    cod_orgao,
                    orgi_nm_orgao,
                    acervo_fim,
                    acervo_inicio,
                    (acervo_fim - acervo_inicio)/acervo_inicio as variacao
                FROM (
                    SELECT
                        tb_data_fim.cod_orgao,
                        SUM(tb_data_fim.acervo) as acervo_fim,
                        SUM(tb_data_inicio.acervo_inicio) as acervo_inicio
                        FROM {namespace}.tb_acervo tb_data_fim
                    INNER JOIN (
                        SELECT
                            acervo as acervo_inicio,
                            dt_inclusao as data_inicio,
                            cod_orgao,
                            tipo_acervo
                        FROM {namespace}.tb_acervo
                        WHERE dt_inclusao = to_timestamp(
                            '{dt_inicio}', 'yyyy-MM-dd')
                        ) tb_data_inicio
                    ON tb_data_fim.cod_orgao = tb_data_inicio.cod_orgao
                    AND tb_data_fim.tipo_acervo = tb_data_inicio.tipo_acervo
                    INNER JOIN {namespace}.tb_regra_negocio_investigacao regras
                    ON regras.cod_atribuicao = tb_data_fim.cod_atribuicao
                        AND regras.classe_documento = tb_data_fim.tipo_acervo
                    WHERE tb_data_fim.dt_inclusao = to_timestamp(
                        '{dt_fim}', 'yyyy-MM-dd')
                    GROUP BY tb_data_fim.cod_orgao
                    ) t
                INNER JOIN exadata.orgi_orgao ON orgi_orgao.orgi_dk = cod_orgao
                WHERE cod_orgao IN (
                    SELECT cast(id_orgao as int)
                    FROM cluster.atualizacao_pj_pacote A
                    INNER JOIN (
                        SELECT cod_pct
                        FROM cluster.atualizacao_pj_pacote
                        WHERE id_orgao = '{orgao_id}') B
                    ON A.cod_pct = B.cod_pct)
                ORDER BY variacao DESC
                LIMIT {n};
                """.format(
                    namespace=settings.TABLE_NAMESPACE,
                    orgao_id=orgao_id,
                    dt_inicio=dt_inicio,
                    dt_fim=dt_fim,
                    n=n
                )
        return run_query(query)

    def get(self, request, *args, **kwargs):
        orgao_id = int(self.kwargs['orgao_id'])
        dt_inicio = str(self.kwargs['dt_inicio'])
        dt_fim = str(self.kwargs['dt_fim'])
        n = int(self.kwargs['n'])

        data = self.get_acervo_increase_topn(
            orgao_id=orgao_id,
            dt_inicio=dt_inicio,
            dt_fim=dt_fim,
            n=n
        )

        if not data:
            raise Http404

        fields = [
            'cod_orgao',
            'nm_orgao',
            'acervo_fim',
            'acervo_inicio',
            'variacao'
        ]
        data_obj = [
            {fieldname: value for fieldname, value in zip(fields, row)}
            for row in data]
        data = AcervoVariationTopNSerializer(data_obj, many=True).data
        return Response(data)


@method_decorator(
    cache_page(300, key_prefix="dominio_outliers"),
    name="dispatch"
)
class OutliersView(APIView):

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
                WHERE A.cod_orgao = {orgao_id}
                AND B.dt_inclusao = to_timestamp('{dt_calculo}', 'yyyy-MM-dd')
                """.format(
                    namespace=settings.TABLE_NAMESPACE,
                    orgao_id=orgao_id,
                    dt_calculo=dt_calculo
                )
        return run_query(query)

    def get(self, request, *args, **kwargs):
        orgao_id = int(self.kwargs['orgao_id'])
        dt_calculo = str(self.kwargs['dt_calculo'])

        data = self.get_outliers(
            orgao_id=orgao_id,
            dt_calculo=dt_calculo
        )

        if not data:
            raise Http404

        fields = ['cod_atribuicao', 'minimo', 'maximo',
                  'media', 'primeiro_quartil', 'mediana', 'terceiro_quartil',
                  'iqr', 'lout', 'hout']
        data_obj = {
            fieldname: value for fieldname, value in zip(fields, data[0])
        }
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
                WHERE id_orgao = {orgao_id}
                """.format(
                    orgao_id=orgao_id,
                    namespace=settings.TABLE_NAMESPACE
                )

        return run_query(query)

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

    def get_entradas(self, orgao_id, cod_matricula):

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
                WHERE comb_orga_dk = {orgao_id}
                AND comb_cdmatricula = '{cod_matricula}'
                """.format(
                    orgao_id=orgao_id,
                    cod_matricula=cod_matricula,
                    namespace=settings.TABLE_NAMESPACE
                )

        return run_query(query)

    def get(self, request, *args, **kwargs):
        orgao_id = int(self.kwargs['orgao_id'])
        # Matricula has 8 digits, with leading zeros
        cod_matricula = str(int(self.kwargs['cod_matricula'])).zfill(8)

        data = self.get_entradas(
            orgao_id=orgao_id,
            cod_matricula=cod_matricula
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


class SuaMesa:
    @ring.lru()
    @staticmethod
    def get_regras(orgao_id, tipo='investigacao'):
        """Busca as regras de negócio relativas a investigação ou processo,
        para um dado órgão.

        Arguments:
            orgao_id {integer} -- ID do órgão a ser procurado.

        Keyword Arguments:
            tipo {str} -- Tipo de regra a ser procurada.
            Pode ser 'investigacao' ou 'processo'. (default: {'investigacao'})

        Returns:
            List[integer] -- Lista de IDs de classes de documentos.
        """
        table_switcher = {
            'investigacao': 'tb_regra_negocio_investigacao',
            'processo': 'tb_regra_negocio_processo'
        }
        regras_table = table_switcher.get(tipo, None)

        if not regras_table:
            # Melhor fazer de outra forma? Raise error?
            return None

        query = """
            SELECT r.classe_documento
            FROM {namespace}.atualizacao_pj_pacote pct
            JOIN {namespace}.{regras_table} r
            ON r.cod_atribuicao = pct.cod_pct
            WHERE pct.id_orgao = {orgao_id}
        """.format(
            orgao_id=orgao_id,
            regras_table=regras_table,
            namespace=settings.TABLE_NAMESPACE
        )

        result = run_query(query)
        return [row[0] for row in result] if result else []


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

        regras_investigacoes = SuaMesa.get_regras(
            orgao_id,
            tipo='investigacao'
        )
        doc_count = Documento.investigacoes.em_curso(
            orgao_id, regras_investigacoes).count()

        return Response(data={"suamesa_investigacoes": doc_count})


class SuaMesaProcessos(APIView):
    def get(self, request, *args, **kwargs):
        orgao_id = int(kwargs.get("orgao_id"))

        regras_processos = SuaMesa.get_regras(orgao_id, tipo='processo')
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

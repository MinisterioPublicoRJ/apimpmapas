from django.http import Http404
from rest_framework.response import Response
from rest_framework.views import APIView

from .db_connectors import run_query
from .serializers import (
    AcervoSerializer,
    SaidasSerializer,
    AcervoVariationSerializer,
    AcervoVariationTopNSerializer,
    OutliersSerializer
)
from lupa.exceptions import QueryError


class AcervoView(APIView):

    def get_acervo(self, orgao_id, tipo_acervo, data):
        query = (
            "SELECT acervo "
            "FROM exadata_aux.tb_acervo "
            "WHERE cod_orgao = {orgao_id} "
            "AND tipo_acervo = {tipo_acervo} "
            "AND dt_inclusao = to_timestamp('{data}', 'yyyy-MM-dd')"
            .format(
                orgao_id=orgao_id,
                tipo_acervo=tipo_acervo,
                data=data
            ))
        return run_query(query)

    def get(self, request, *args, **kwargs):
        orgao_id = int(self.kwargs['orgao_id'])
        tipo_acervo = int(self.kwargs['tipo_acervo'])
        data = str(self.kwargs['data'])

        acervo_qtd = self.get_acervo(
            orgao_id=orgao_id,
            tipo_acervo=tipo_acervo,
            data=data
        )

        if not acervo_qtd:
            raise Http404

        acervo = {'acervo_qtd': acervo_qtd}
        data = AcervoSerializer(acervo).data
        return Response(data)


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
                FROM exadata_aux.tb_acervo tb_data_fim
                INNER JOIN (
                    SELECT
                        acervo as acervo_inicio,
                        dt_inclusao as data_inicio,
                        cod_orgao,
                        tipo_acervo
                    FROM exadata_aux.tb_acervo
                    WHERE dt_inclusao = to_timestamp(
                        '{dt_inicio}', 'yyyy-MM-dd')
                    ) tb_data_inicio
                ON tb_data_fim.cod_orgao = tb_data_inicio.cod_orgao
                    AND tb_data_fim.tipo_acervo = tb_data_inicio.tipo_acervo
                INNER JOIN exadata_aux.tb_regra_negocio_investigacao regras
                ON regras.cod_atribuicao = tb_data_fim.cod_atribuicao
                    AND regras.classe_documento = tb_data_fim.tipo_acervo
                WHERE tb_data_fim.dt_inclusao = to_timestamp(
                    '{dt_fim}', 'yyyy-MM-dd')
                AND tb_data_fim.cod_orgao = {orgao_id}) t
            """.format(
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
        data_obj = {fieldname: value for fieldname, value in zip(fields, data)}
        data = AcervoVariationSerializer(data_obj).data
        return Response(data)


class AcervoVariationTopNView(APIView):
    queryset = ''

    def get_acervo_increase_topn(self, orgao_id, dt_inicio, dt_fim, n=3):
        query ="""
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
                        FROM exadata_aux.tb_acervo tb_data_fim
                    INNER JOIN (
                        SELECT
                            acervo as acervo_inicio,
                            dt_inclusao as data_inicio,
                            cod_orgao,
                            tipo_acervo
                        FROM exadata_aux.tb_acervo
                        WHERE dt_inclusao = to_timestamp(
                            '{dt_inicio}', 'yyyy-MM-dd')
                        ) tb_data_inicio
                    ON tb_data_fim.cod_orgao = tb_data_inicio.cod_orgao
                    AND tb_data_fim.tipo_acervo = tb_data_inicio.tipo_acervo
                    INNER JOIN exadata_aux.tb_regra_negocio_investigacao regras
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

        fields = ['cod_orgao', 'nm_orgao', 'acervo_fim', 'acervo_inicio', 'variacao']
        data_obj = [
            {fieldname: value for fieldname, value in zip(fields, row)}
            for row in data]
        data = AcervoVariationTopNSerializer(data_obj, many=True).data
        return Response(data)


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
                FROM exadata_aux.tb_acervo A
                INNER JOIN exadata_aux.tb_distribuicao B
                ON A.cod_atribuicao = B.cod_atribuicao
                AND A.dt_inclusao = B.dt_inclusao
                WHERE A.cod_orgao = {orgao_id}
                AND B.dt_inclusao = to_timestamp('{dt_calculo}', 'yyyy-MM-dd')
                """.format(
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
        data_obj = {fieldname: value for fieldname, value in zip(fields, data)}
        data = OutliersSerializer(data_obj).data
        return Response(data)


class SaidasView(APIView):

    def get_saidas(self, orgao_id):

        query = """
                SELECT saidas, id_orgao, cod_pct, percent_rank, dt_calculo
                FROM exadata_aux.tb_saida
                WHERE id_orgao = {orgao_id}
                """.format(orgao_id=orgao_id)

        return run_query(query)

    def get(self, request, *args, **kwargs):
        orgao_id = int(self.kwargs['orgao_id'])

        data = self.get_saidas(
            orgao_id=orgao_id
        )

        if not data:
            raise Http404

        fields = ['saidas', 'id_orgao', 'cod_pct', 'percent_rank', 'dt_calculo']
        data_obj = {fieldname: value for fieldname, value in zip(fields, data)}
        data = SaidasSerializer(data_obj).data
        return Response(data)

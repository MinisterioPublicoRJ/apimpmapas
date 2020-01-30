from django.http import Http404
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.response import Response

from .db_connectors import execute
from .serializers import (
    AcervoSerializer,
    AcervoVariationSerializer,
    AcervoVariationTopNSerializer  # , AlertaSerializer
)
from lupa.exceptions import QueryError


# Create your views here.
# class AlertasListView(ListAPIView):
#     queryset = Alerta.objects.all()
#     serializer_class = AlertaSerializer


class AcervoView(RetrieveAPIView):

    def get_acervo(self, orgao_id, tipo_acervo, data):

        try:
            db_result = execute(
                "SELECT acervo "
                "FROM exadata_aux.tb_acervo "
                "WHERE cod_orgao = {orgao_id} "
                "AND tipo_acervo = {tipo_acervo} "
                "AND dt_inclusao = to_timestamp('{data}', 'yyyy-MM-dd')"
                .format(
                    orgao_id=orgao_id,
                    tipo_acervo=tipo_acervo,
                    data=data
                )
            )
        except QueryError:
            return None

        if db_result and db_result[0]:
            return db_result[0][0]

        return None

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
        print(acervo)
        data = AcervoSerializer(acervo).data
        return Response(data)


class AcervoVariationView(RetrieveAPIView):

    def get_acervo_increase(self, orgao_id, tipo_acervo, dt_inicio, dt_fim):
        try:
            db_result = execute(
                """
                SELECT
                    tb_data_fim.acervo as acervo_fim,
                    tb_data_inicio.acervo_inicio,
                    (acervo - acervo_inicio)/acervo_inicio as variacao
                FROM exadata_aux.tb_acervo tb_data_fim
                INNER JOIN (
                    SELECT
                        acervo as acervo_inicio,
                        dt_inclusao as data_inicio,
                        cod_orgao,
                        tipo_acervo
                    FROM exadata_aux.tb_acervo
                    WHERE dt_inclusao = to_timestamp('{dt_inicio}', 'yyyy-MM-dd')
                    ) tb_data_inicio
                ON tb_data_fim.cod_orgao = tb_data_inicio.cod_orgao
                AND tb_data_fim.tipo_acervo = tb_data_inicio.tipo_acervo
                WHERE tb_data_fim.dt_inclusao = to_timestamp(
                    '{dt_fim}', 'yyyy-MM-dd')
                AND tb_data_fim.cod_orgao = {orgao_id}
                AND tb_data_fim.tipo_acervo = {tipo_acervo};
                """
                .format(
                    orgao_id=orgao_id,
                    tipo_acervo=tipo_acervo,
                    dt_inicio=dt_inicio,
                    dt_fim=dt_fim
                )
            )
        except QueryError:
            return None

        if db_result and db_result[0]:
            return db_result[0]

        return None

    def get(self, request, *args, **kwargs):
        orgao_id = int(self.kwargs['orgao_id'])
        tipo_acervo = int(self.kwargs['tipo_acervo'])
        dt_inicio = str(self.kwargs['dt_inicio'])
        dt_fim = str(self.kwargs['dt_fim'])

        data = self.get_acervo_increase(
            orgao_id=orgao_id,
            tipo_acervo=tipo_acervo,
            dt_inicio=dt_inicio,
            dt_fim=dt_fim
        )

        if not data:
            raise Http404

        fields = ['acervo_fim', 'acervo_inicio', 'variacao']
        data_obj = {fieldname: value for fieldname, value in zip(fields, data)}
        data = AcervoVariationSerializer(data_obj).data
        return Response(data)


class AcervoVariationTopNView(ListAPIView):
    queryset = ''

    def get_acervo_increase_topn(self, tipo_acervo, dt_inicio, dt_fim, n=3):
        try:
            db_result = execute(
                """
                SELECT
                    tb_data_fim.acervo as acervo_fim,
                    tb_data_inicio.acervo_inicio,
                    (acervo - acervo_inicio)/acervo_inicio as variacao,
                    tb_data_fim.cod_orgao as cod_orgao
                FROM exadata_aux.tb_acervo tb_data_fim
                INNER JOIN (
                    SELECT
                        acervo as acervo_inicio,
                        dt_inclusao as data_inicio,
                        cod_orgao,
                        tipo_acervo
                    FROM exadata_aux.tb_acervo
                    WHERE dt_inclusao = to_timestamp('{dt_inicio}', 'yyyy-MM-dd')
                    ) tb_data_inicio
                ON tb_data_fim.cod_orgao = tb_data_inicio.cod_orgao
                AND tb_data_fim.tipo_acervo = tb_data_inicio.tipo_acervo
                WHERE tb_data_fim.dt_inclusao = to_timestamp(
                    '{dt_fim}', 'yyyy-MM-dd')
                AND tb_data_fim.tipo_acervo = {tipo_acervo}
                ORDER BY variacao DESC
                LIMIT {n};
                """
                .format(
                    tipo_acervo=tipo_acervo,
                    dt_inicio=dt_inicio,
                    dt_fim=dt_fim,
                    n=n
                )
            )
        except QueryError:
            return None

        if db_result and db_result[0]:
            return db_result

        return None

    def get(self, request, *args, **kwargs):
        tipo_acervo = int(self.kwargs['tipo_acervo'])
        dt_inicio = str(self.kwargs['dt_inicio'])
        dt_fim = str(self.kwargs['dt_fim'])
        n = int(self.kwargs['n'])

        data = self.get_acervo_increase_topn(
            tipo_acervo=tipo_acervo,
            dt_inicio=dt_inicio,
            dt_fim=dt_fim,
            n=n
        )

        if not data:
            raise Http404

        fields = ['acervo_fim', 'acervo_inicio', 'variacao', 'cod_orgao']
        data_obj = [
            {fieldname: value for fieldname, value in zip(fields, row)}
            for row in data]
        data = AcervoVariationTopNSerializer(data_obj, many=True).data
        return Response(data)

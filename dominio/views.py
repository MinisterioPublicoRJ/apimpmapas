from django.http import Http404
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.response import Response

from .db_connectors import execute
from .serializers import AcervoSerializer  # , AlertaSerializer
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
                "FROM exadata_aux.vw_acervo_historico_diario "
                "WHERE cod_orgao = {orgao_id} "
                "AND tipo_acervo = {tipo_acervo} "
                "AND `data` = to_timestamp('{data}', 'yyyy-MM-dd')"
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

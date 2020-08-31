from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response

from dominio.db_connectors import get_hbase_table
from dominio.mixins import CacheMixin, PaginatorMixin, JWTAuthMixin
from dominio.models import Alerta
from dominio.alertas import dao
from dominio.utils import hbase_encode_row

from .serializers import AlertasListaSerializer


# TODO: criar um endpoint unificado?
class AlertasView(JWTAuthMixin, CacheMixin, PaginatorMixin, APIView):
    cache_config = 'ALERTAS_CACHE_TIMEOUT'
    # TODO: Mover constante para um lugar decente
    # ALERTAS_SIZE = 25

    def get(self, request, *args, **kwargs):
        orgao_id = int(kwargs.get(self.orgao_url_kwarg))
        # page = int(request.GET.get("page", 1))
        tipo_alerta = request.GET.get("tipo_alerta", None)

        data = Alerta.validos_por_orgao(orgao_id, tipo_alerta)
        # page_data = self.paginate(
        #     data,
        #     page=page,
        #     page_size=self.ALERTAS_SIZE
        # )
        alertas_lista = AlertasListaSerializer(data, many=True)

        return Response(data=alertas_lista.data)


class ResumoAlertasView(JWTAuthMixin, CacheMixin, PaginatorMixin, APIView):
    cache_config = 'ALERTAS_CACHE_TIMEOUT'

    def get(self, request, *args, **kwargs):
        orgao_id = int(kwargs.get(self.orgao_url_kwarg))

        alertas_resumo = dao.ResumoAlertasDAO.get_all(id_orgao=orgao_id)

        return Response(data=alertas_resumo)


class AlertasComprasView(JWTAuthMixin, CacheMixin, PaginatorMixin, APIView):
    cache_config = 'ALERTAS_COMPRAS_CACHE_TIMEOUT'

    def get(self, request, *args, **kwargs):
        id_orgao = int(kwargs.get(self.orgao_url_kwarg))
        data = dao.AlertaComprasDAO.get(id_orgao=id_orgao, accept_empty=True)
        return Response(data=data)


class DispensarAlertaView(JWTAuthMixin, APIView):
    def get_hbase_key(self, orgao_id, sigla_alerta, alerta_id):
        return f"{orgao_id}_{sigla_alerta}_{alerta_id}"

    def get_hbase_row(self):
        orgao_id = self.kwargs.get("orgao_id")
        sigla = self.kwargs.get("sigla")
        alerta_id = self.request.GET.get("alerta_id")

        key = self.get_hbase_key(orgao_id, sigla, alerta_id)
        data = {
            "orgao": orgao_id,
            "sigla": sigla,
            "alerta_id": alerta_id,
        }
        return hbase_encode_row((key, data))

    def post(self, request, *args, **kwargs):
        # TODO: criar serializador para dados da requisição
        hbase_table = get_hbase_table(settings.HBASE_DISPENSAR_ALERTAS_TABLE)
        hbase_table.put(*self.get_hbase_row())
        return Response(data={})

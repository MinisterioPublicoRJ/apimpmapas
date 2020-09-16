from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response

from dominio.db_connectors import get_hbase_table
from dominio.mixins import CacheMixin, PaginatorMixin, JWTAuthMixin
from dominio.alertas import dao
from dominio.utils import hbase_encode_row

from .serializers import AlertasListaSerializer, IdentificadorAlertaSerializer


# TODO: criar um endpoint unificado?
class AlertasView(JWTAuthMixin, CacheMixin, PaginatorMixin, APIView):
    cache_config = 'ALERTAS_CACHE_TIMEOUT'
    # TODO: Mover constante para um lugar decente
    # ALERTAS_SIZE = 25

    def get(self, request, *args, **kwargs):
        orgao_id = int(kwargs.get(self.orgao_url_kwarg))
        # page = int(request.GET.get("page", 1))
        tipo_alerta = request.GET.get("tipo_alerta", None)

        data = dao.AlertaMGPDAO.get(
            orgao_id=orgao_id,
            tipo_alerta=tipo_alerta,
        )
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


class AlertasComprasView(JWTAuthMixin, PaginatorMixin, APIView):
    cache_config = 'ALERTAS_COMPRAS_CACHE_TIMEOUT'

    def get(self, request, *args, **kwargs):
        id_orgao = int(kwargs.get(self.orgao_url_kwarg))
        data = dao.AlertaComprasDAO.get(id_orgao=id_orgao, accept_empty=True)
        return Response(data=data)


class ITsGateView(JWTAuthMixin, CacheMixin, APIView):
    cache_config = 'ITS_GATE_CACHE_TIMEOUT'

    def get(self, request, *args, **kwargs):
        docu_dk = int(kwargs.get(self.orgao_url_kwarg))
        data = dao.ITGateDAO.get(docu_dk=docu_dk)
        return Response(data=data)


class DispensarAlertaView(JWTAuthMixin, APIView):
    def get_alerta_id(self):
        ser = IdentificadorAlertaSerializer(data=self.request.GET)
        ser.is_valid(raise_exception=True)
        return ser.validated_data["alerta_id"]

    def get_hbase_key(self, orgao_id, sigla_alerta, alerta_id):
        return f"{orgao_id}_{sigla_alerta}_{alerta_id}"

    def prepare_hbase_row(self):
        sigla = "COMP"
        orgao_id = self.kwargs.get(self.orgao_url_kwarg)
        alerta_id = self.get_alerta_id()

        key = self.get_hbase_key(orgao_id, sigla, alerta_id)
        data = {
            "dados_alertas:orgao": orgao_id,
            "dados_alertas:sigla": sigla,
            "dados_alertas:alerta_id": alerta_id,
        }
        return hbase_encode_row((key, data))

    def post(self, request, *args, **kwargs):
        row = self.prepare_hbase_row()
        hbase_table = get_hbase_table(
            settings.PROMOTRON_HBASE_NAMESPACE
            +
            settings.HBASE_DISPENSAR_ALERTAS_TABLE
        )
        hbase_table.put(*row)
        return Response(
            data={"detail": "Alerta dispensado com sucesso"},
            status=201
        )


class RetornarAlertaView(JWTAuthMixin, APIView):
    def get_alerta_id(self):
        ser = IdentificadorAlertaSerializer(data=self.request.GET)
        ser.is_valid(raise_exception=True)
        return ser.validated_data["alerta_id"]

    def get_hbase_key(self, orgao_id, sigla_alerta, alerta_id):
        return f"{orgao_id}_{sigla_alerta}_{alerta_id}".encode()

    def post(self, request, *args, **kwargs):
        sigla = "COMP"
        orgao_id = self.kwargs.get(self.orgao_url_kwarg)
        alerta_id = self.get_alerta_id()

        hbase_table = get_hbase_table(
            settings.PROMOTRON_HBASE_NAMESPACE
            +
            settings.HBASE_DISPENSAR_ALERTAS_TABLE
        )
        hbase_table.delete(self.get_hbase_key(orgao_id, sigla, alerta_id))

        return Response(
            data={"detail": "Alerta retornado com sucesso"},
            status=200
        )

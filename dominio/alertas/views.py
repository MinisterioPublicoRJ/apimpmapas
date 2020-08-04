from rest_framework.views import APIView
from rest_framework.response import Response

from dominio.mixins import CacheMixin, PaginatorMixin, JWTAuthMixin
from dominio.models import Alerta
from dominio.alertas.dao import AlertaComprasDAO

from .serializers import AlertasListaSerializer, AlertasResumoSerializer


class AlertasView(JWTAuthMixin, CacheMixin, PaginatorMixin, APIView):
    cache_config = 'ALERTAS_CACHE_TIMEOUT'
    # TODO: Mover constante para um lugar decente
    # ALERTAS_SIZE = 25

    def get(self, request, *args, **kwargs):
        orgao_id = int(kwargs.get("orgao_id"))
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
        orgao_id = int(kwargs.get("orgao_id"))

        data = Alerta.resumo_por_orgao(orgao_id)
        alertas_resumo = AlertasResumoSerializer(data, many=True)

        return Response(data=alertas_resumo.data)


class AlertasComprasView(JWTAuthMixin, CacheMixin, PaginatorMixin, APIView):
    cache_config = 'ALERTAS_COMPRAS_CACHE_TIMEOUT'

    def get(self, request, *args, **kwargs):
        id_orgao = int(kwargs.get("orgao_id"))
        data = AlertaComprasDAO.get(id_orgao=id_orgao, accept_empty=True)
        return Response(data=data)

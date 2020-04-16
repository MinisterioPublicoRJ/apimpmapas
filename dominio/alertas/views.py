from rest_framework.views import APIView
from rest_framework.response import Response

from dominio.mixins import CacheMixin, PaginatorMixin, JWTAuthMixin
from dominio.models import Alerta

from .serializers import AlertasListaSerializer


class AlertasView(JWTAuthMixin, CacheMixin, PaginatorMixin, APIView):
    cache_config = 'ALERTAS_CACHE_TIMEOUT'
    # TODO: Mover constante para um lugar decente
    ALERTAS_SIZE = 25

    def get(self, request, *args, **kwargs):
        orgao_id = int(kwargs.get("orgao_id"))
        page = int(request.GET.get("page", 1))

        data = Alerta.validos_por_orgao(orgao_id)
        page_data = self.paginate(
            data,
            page=page,
            page_size=self.ALERTAS_SIZE
        )

        alertas_lista = AlertasListaSerializer(page_data, many=True)

        return Response(data=alertas_lista.data)

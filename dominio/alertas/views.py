from rest_framework.views import APIView
from rest_framework.response import Response

from dominio.mixins import CacheMixin, PaginatorMixin, JWTAuthMixin
from dominio.alertas import controllers, dao

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


class DispensarAlertaView(JWTAuthMixin, APIView):
    def get_alerta_id(self):
        ser = IdentificadorAlertaSerializer(data=self.request.GET)
        ser.is_valid(raise_exception=True)
        return ser.validated_data["alerta_id"]

    def post(self, request, *args, **kwargs):
        orgao_id = self.kwargs.get(self.orgao_url_kwarg)
        alerta_id = self.get_alerta_id()

        controllers.DispensaAlertaComprasCotroller.dispensa_para_orgao(
            orgao_id, alerta_id
        )
        return Response(
            data={"detail": "Alerta dispensado com sucesso"},
            status=201
        )


class RetornarAlertaView(JWTAuthMixin, APIView):
    def get_alerta_id(self):
        ser = IdentificadorAlertaSerializer(data=self.request.GET)
        ser.is_valid(raise_exception=True)
        return ser.validated_data["alerta_id"]

    def post(self, request, *args, **kwargs):
        orgao_id = self.kwargs.get(self.orgao_url_kwarg)
        alerta_id = self.get_alerta_id()

        controllers.DispensaAlertaComprasCotroller.retorna_para_orgao(
            orgao_id, alerta_id
        )

        return Response(
            data={"detail": "Alerta retornado com sucesso"},
            status=200
        )


class EnviarAlertaComprasOuvidoriaView(JWTAuthMixin, APIView):
    def get_alerta_id(self):
        ser = IdentificadorAlertaSerializer(data=self.request.GET)
        ser.is_valid(raise_exception=True)
        return ser.validated_data["alerta_id"]

    def post(self, request, *args, **kwargs):
        orgao_id = self.kwargs.get(self.orgao_url_kwarg)
        alerta_id = self.get_alerta_id()

        controller = controllers.EnviaAlertaComprasOuvidoriaController(
            orgao_id,
            alerta_id
        )
        resp, status = controller.envia()
        return Response(data=resp, status=status)

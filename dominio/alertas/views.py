from rest_framework.views import APIView
from rest_framework.response import Response

from dominio.mixins import CacheMixin, PaginatorMixin, JWTAuthMixin
from dominio.alertas import dao
from dominio.alertas.controllers import (
    DispensaAlertaController,
    EnviaAlertaComprasOuvidoriaController,
    EnviaAlertaISPSOuvidoriaController,
)
from dominio.alertas.exceptions import (
    APIInvalidAlertaSigla,
)
from dominio.permissions import PromotorOnlyPermission


# TODO: criar um endpoint unificado?
class AlertasView(JWTAuthMixin, PaginatorMixin, APIView):
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

        return Response(data=data)


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
    # TODO: get_object que retorna 404 se alerta não existir
    def post(self, request, *args, **kwargs):
        orgao_id = self.kwargs.get(self.orgao_url_kwarg)
        alerta_id = self.kwargs.get("alerta_id")

        controller = DispensaAlertaController(
            orgao_id,
            alerta_id
        )
        controller.dispensa_para_orgao()
        return Response(
            data={"detail": "Alerta dispensado com sucesso"},
            status=201
        )


class RetornarAlertaView(JWTAuthMixin, APIView):
    # TODO: get_object que retorna 404 se alerta não existir
    def post(self, request, *args, **kwargs):
        orgao_id = self.kwargs.get(self.orgao_url_kwarg)
        alerta_id = self.kwargs.get("alerta_id")

        controller = DispensaAlertaController(
            orgao_id,
            alerta_id,
        )
        controller.retorna_para_orgao()

        return Response(
            data={"detail": "Alerta retornado com sucesso"},
            status=200
        )


class AlertasOverlayView(JWTAuthMixin, CacheMixin, APIView):
    cache_config = 'ALERTAS_OVERLAY_CACHE_TIMEOUT'

    def get(self, request, *args, **kwargs):
        docu_dk = int(kwargs.get('docu_dk'))
        data = dao.AlertasOverlayDAO.get(docu_dk=docu_dk, request=request)
        return Response(data=data)


class EnviarAlertaOuvidoriaView(JWTAuthMixin, APIView):
    # TODO: get_object que retorna 404 se alerta não existir
    permission_classes = [PromotorOnlyPermission]

    def controller_router(self, sigla_alerta):
        sigla_alerta = sigla_alerta.lower()
        controllers = {
            "comp": EnviaAlertaComprasOuvidoriaController,
            "isps": EnviaAlertaISPSOuvidoriaController,
        }
        if sigla_alerta not in controllers:
            raise APIInvalidAlertaSigla

        return controllers[sigla_alerta]

    def post(self, request, *args, **kwargs):
        orgao_id = self.kwargs.get(self.orgao_url_kwarg)
        sigla_alerta = self.kwargs.get("sigla_alerta")
        alerta_id = self.kwargs.get("alerta_id")

        controller = self.controller_router(sigla_alerta)(
            orgao_id,
            alerta_id
        )
        resp, status = controller.envia()
        return Response(data=resp, status=status)


class BaixarAlertasView(JWTAuthMixin, APIView):
    def get(self, request, *args, **kwargs):
        orgao_id = int(kwargs.get(self.orgao_url_kwarg))
        tipo_alerta = request.GET.get("tipo_alerta", None)

        return dao.BaixarAlertasDAO.get(
            alrt_type=tipo_alerta,
            accept_empty=False,
            orgao_id=orgao_id,
        )

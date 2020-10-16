from rest_framework.response import Response
from rest_framework.views import APIView

from dominio.mixins import CacheMixin, JWTAuthMixin, PaginatorMixin
from dominio.pip.dao import (
    PIPComparadorRadaresDAO,
    PIPIndicadoresDeSucessoDAO,
    PIPRadarPerformanceDAO,
    PIPPrincipaisInvestigadosDAO,
    PIPPrincipaisInvestigadosListaDAO,
    PIPPrincipaisInvestigadosPerfilDAO,
)


class PIPIndicadoresDeSucessoView(JWTAuthMixin, CacheMixin, APIView):
    cache_config = "PIP_INDICADORES_SUCESSO_CACHE_TIMEOUT"

    def get(self, request, *args, **kwargs):
        orgao_id = int(kwargs.get(self.orgao_url_kwarg))
        data = PIPIndicadoresDeSucessoDAO.get(orgao_id=orgao_id)
        return Response(data=data)


class PIPRadarPerformanceView(JWTAuthMixin, CacheMixin, APIView):
    cache_config = "PIP_RADAR_PERFORMANCE_CACHE_TIMEOUT"

    def get(self, *args, **kwargs):
        orgao_id = int(kwargs.get(self.orgao_url_kwarg))
        return Response(data=PIPRadarPerformanceDAO.get(orgao_id=orgao_id))


class PIPPrincipaisInvestigadosView(
        JWTAuthMixin, PaginatorMixin, APIView):
    cache_config = "PIP_PRINCIPAIS_INVESTIGADOS_CACHE_TIMEOUT"
    PRINCIPAIS_INVESTIGADOS_SIZE = 20

    def get(self, request, *args, **kwargs):
        orgao_id = kwargs.get(self.orgao_url_kwarg)
        cpf = kwargs.get("cpf")
        page = int(request.GET.get("page", 1))

        data = PIPPrincipaisInvestigadosDAO.get(orgao_id=orgao_id, cpf=cpf)

        page_data = self.paginate(
            data,
            page=page,
            page_size=self.PRINCIPAIS_INVESTIGADOS_SIZE
        )

        return Response(page_data)

    def post(self, request, *args, **kwargs):
        orgao_id = kwargs.get(self.orgao_url_kwarg)
        cpf = kwargs.get("cpf")

        # TODO: Verificar que o post foi feito pelo mesmo orgao
        action = request.POST.get("action")
        representante_dk = request.POST.get("representante_dk")

        # Nome de personagem é necessário para a chave do HBase
        if not representante_dk:
            raise ValueError("Campo 'representante_dk' não foi dado!")
        if not action:
            raise ValueError("Campo 'action' não foi dado!")

        data = PIPPrincipaisInvestigadosDAO.save_hbase_flags(
            orgao_id, cpf, representante_dk, action)

        return Response(data)


class PIPPrincipaisInvestigadosListaView(
        JWTAuthMixin, PaginatorMixin, APIView):
    cache_config = "PIP_PRINCIPAIS_INVESTIGADOS_LISTA_CACHE_TIMEOUT"
    PRINCIPAIS_INVESTIGADOS_PROCEDIMENTOS_SIZE = 20

    def get(self, request, *args, **kwargs):
        representante_dk = int(kwargs.get("representante_dk"))
        page = int(request.GET.get("page", 1))
        pess_dk = int(request.GET.get("pess_dk", 0))

        similares = PIPPrincipaisInvestigadosPerfilDAO.get(dk=representante_dk)
        perfil = PIPPrincipaisInvestigadosPerfilDAO.get_header_info(similares)
        procedimentos = PIPPrincipaisInvestigadosListaDAO.get(
            dk=representante_dk, pess_dk=pess_dk
        )

        page_data = self.paginate(
            procedimentos,
            page=page,
            page_size=self.PRINCIPAIS_INVESTIGADOS_PROCEDIMENTOS_SIZE
        )

        data = {
            'perfil': perfil,
            'similares': similares,
            'procedimentos': page_data
        }

        return Response(data)


class PIPComparadorRadaresView(JWTAuthMixin, APIView):
    def get(self, request, *args, **kwargs):
        orgao_id = int(self.kwargs.get(self.orgao_url_kwarg))
        return Response(data=PIPComparadorRadaresDAO.get(orgao_id=orgao_id))

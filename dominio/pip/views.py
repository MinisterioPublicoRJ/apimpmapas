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
        # page = int(request.GET.get("page", 1))
        pess_dk = int(request.GET.get("pess_dk", 0))
        tipo_orgao = request.GET.get("orgao_type", "pip")

        # Filtra os procedimentos por determinados pacotes
        # No futuro, isso poderá ser retirado
        if tipo_orgao == "pip":
            pcts = (200, 201, 202, 203, 204, 205, 206, 207, 208, 209)
        elif tipo_orgao == "tutela":
            pcts = (20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33,
                    180, 181, 182, 183)
        else:
            pcts = (-1,)

        # Usado para acessar a partição correta
        digit = int(str(representante_dk)[-1])

        similares = PIPPrincipaisInvestigadosPerfilDAO.get(
            dk=representante_dk, pcts=pcts, digit=digit)
        perfil = PIPPrincipaisInvestigadosPerfilDAO.get_header_info(similares)
        procedimentos = PIPPrincipaisInvestigadosListaDAO.get(
            dk=representante_dk, pess_dk=pess_dk, pcts=pcts, digit=digit
        )

        # Tirar a paginação por enquanto
        # procedimentos = self.paginate(
        #     procedimentos,
        #     page=page,
        #     page_size=self.PRINCIPAIS_INVESTIGADOS_PROCEDIMENTOS_SIZE
        # )

        data = {
            'perfil': perfil,
            'similares': similares,
            'procedimentos': procedimentos
        }

        return Response(data)


class PIPComparadorRadaresView(JWTAuthMixin, APIView):
    def get(self, request, *args, **kwargs):
        orgao_id = int(self.kwargs.get(self.orgao_url_kwarg))
        return Response(data=PIPComparadorRadaresDAO.get(orgao_id=orgao_id))

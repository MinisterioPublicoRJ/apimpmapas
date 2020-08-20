from rest_framework.response import Response
from rest_framework.views import APIView

from dominio.mixins import CacheMixin, JWTAuthMixin, PaginatorMixin
from dominio.models import Vista, Documento
from dominio.pip.dao import (
    PIPDetalheAproveitamentosDAO,
    PIPIndicadoresDeSucessoDAO,
    PIPRadarPerformanceDAO,
    PIPPrincipaisInvestigadosDAO,
    PIPPrincipaisInvestigadosListaDAO,
)
from dominio.pip.utils import get_orgaos_same_aisps


class PIPDetalheAproveitamentosView(JWTAuthMixin, CacheMixin, APIView):
    cache_config = "PIP_DETALHEAPROVEITAMENTOS_CACHE_TIMEOUT"

    def get(self, request, *args, **kwargs):
        orgao_id = int(self.kwargs.get(self.orgao_url_kwarg))

        data = PIPDetalheAproveitamentosDAO.get(orgao_id=orgao_id)
        return Response(data)


class PIPVistasAbertasMensalView(JWTAuthMixin, CacheMixin, APIView):
    cache_config = "PIP_VISTASABERTASMENSAL_CACHE_TIMEOUT"

    def get(self, request, *args, **kwargs):
        orgao_id = int(kwargs.get(self.orgao_url_kwarg))
        cpf = kwargs.get("cpf")

        aberturas = Vista.vistas.aberturas_30_dias_PIP(orgao_id, cpf)
        nr_aberturas_30_dias = aberturas.count()
        nr_investigacoes_30_dias = (
            aberturas.filter().values("documento").distinct().count()
        )

        data = {
            "nr_aberturas_30_dias": nr_aberturas_30_dias,
            "nr_investigacoes_30_dias": nr_investigacoes_30_dias,
        }

        return Response(data=data)


# Será substituído pelo dominio.suamesa.views.SuaMesaView
class PIPSuaMesaInvestigacoesAISPView(JWTAuthMixin, CacheMixin, APIView):
    cache_config = "PIP_SUAMESAINVESTIGACOESAISP_CACHE_TIMEOUT"

    def get(self, request, *args, **kwargs):
        orgao_id = int(kwargs.get(self.orgao_url_kwarg))

        _, orgaos_same_aisp = get_orgaos_same_aisps(orgao_id)

        doc_count = Documento.investigacoes.em_curso_pip_aisp(
            orgaos_same_aisp
        ).count()

        data = {"aisp_nr_investigacoes": doc_count}

        return Response(data=data)


class PIPIndicadoresDeSucessoView(JWTAuthMixin, CacheMixin, APIView):
    cache_config = "PIP_INDICADORES_SUCESSO_CACHE_TIMEOUT"

    def get(self, request, *args, **kwargs):
        orgao_id = int(kwargs.get(self.orgao_url_kwarg))
        data = PIPIndicadoresDeSucessoDAO.get(orgao_id=orgao_id)
        return Response(data=data)


# Será substituído pelo dominio.suamesa.views.SuaMesaView
class PIPSuaMesaInqueritosView(JWTAuthMixin, CacheMixin, APIView):
    cache_config = "PIP_SUAMESAINQUERITOS_CACHE_TIMEOUT"

    def get(self, request, *args, **kwargs):
        orgao_id = int(kwargs.get(self.orgao_url_kwarg))

        doc_count = Documento.investigacoes.em_curso(
            orgao_id, [3, 494]
        ).count()

        data = {"pip_nr_inqueritos": doc_count}

        return Response(data=data)


# Será substituído pelo dominio.suamesa.views.SuaMesaView
class PIPSuaMesaPICsView(JWTAuthMixin, CacheMixin, APIView):
    cache_config = "PIP_SUAMESAPICS_CACHE_TIMEOUT"

    def get(self, request, *args, **kwargs):
        orgao_id = int(kwargs.get(self.orgao_url_kwarg))

        doc_count = Documento.investigacoes.em_curso(
            orgao_id, [590]
        ).count()

        data = {"pip_nr_pics": doc_count}

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


class PIPPrincipaisInvestigadosListaView(JWTAuthMixin, CacheMixin, APIView):
    cache_config = "PIP_PRINCIPAIS_INVESTIGADOS_LISTA_CACHE_TIMEOUT"

    def get(self, request, *args, **kwargs):
        representante_dk = int(kwargs.get("representante_dk"))

        data = PIPPrincipaisInvestigadosListaDAO.get(dk=representante_dk)

        return Response(data)

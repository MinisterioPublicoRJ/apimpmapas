from rest_framework.response import Response
from rest_framework.views import APIView

from dominio.mixins import CacheMixin, JWTAuthMixin, PaginatorMixin
from dominio.models import Vista, Documento
from dominio.pip.dao import (
    PIPDetalheAproveitamentosDAO,
    PIPRadarPerformanceDAO,
    PIPPrincipaisInvestigadosDAO,
)
from .utils import get_orgaos_same_aisps


class PIPDetalheAproveitamentosView(JWTAuthMixin, CacheMixin, APIView):
    cache_config = "PIP_DETALHEAPROVEITAMENTOS_CACHE_TIMEOUT"

    def get(self, request, *args, **kwargs):
        orgao_id = int(self.kwargs["orgao_id"])

        data = PIPDetalheAproveitamentosDAO.get(orgao_id=orgao_id)
        return Response(data)


class PIPVistasAbertasMensalView(JWTAuthMixin, CacheMixin, APIView):
    cache_config = "PIP_VISTASABERTASMENSAL_CACHE_TIMEOUT"

    def get(self, request, *args, **kwargs):
        orgao_id = int(kwargs.get("orgao_id"))
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


class PIPSuaMesaInvestigacoesAISPView(JWTAuthMixin, CacheMixin, APIView):
    cache_config = "PIP_SUAMESAINVESTIGACOESAISP_CACHE_TIMEOUT"

    def get(self, request, *args, **kwargs):
        orgao_id = int(kwargs.get("orgao_id"))

        _, orgaos_same_aisp = get_orgaos_same_aisps(orgao_id)

        doc_count = Documento.investigacoes.em_curso_pip_aisp(
            orgaos_same_aisp
        ).count()

        data = {"aisp_nr_investigacoes": doc_count}

        return Response(data=data)


class PIPSuaMesaInqueritosView(JWTAuthMixin, CacheMixin, APIView):
    cache_config = "PIP_SUAMESAINQUERITOS_CACHE_TIMEOUT"

    def get(self, request, *args, **kwargs):
        orgao_id = int(kwargs.get("orgao_id"))

        doc_count = Documento.investigacoes.em_curso(
            orgao_id, [3, 494]
        ).count()

        data = {"pip_nr_inqueritos": doc_count}

        return Response(data=data)


class PIPSuaMesaPICsView(JWTAuthMixin, CacheMixin, APIView):
    cache_config = "PIP_SUAMESAPICS_CACHE_TIMEOUT"

    def get(self, request, *args, **kwargs):
        orgao_id = int(kwargs.get("orgao_id"))

        doc_count = Documento.investigacoes.em_curso(
            orgao_id, [590]
        ).count()

        data = {"pip_nr_pics": doc_count}

        return Response(data=data)


class PIPRadarPerformanceView(JWTAuthMixin, CacheMixin, APIView):
    cache_config = "PIP_RADAR_PERFORMANCE_CACHE_TIMEOUT"

    def get(self, *args, **kwargs):
        orgao_id = int(kwargs.get("orgao_id"))
        return Response(data=PIPRadarPerformanceDAO.get(orgao_id=orgao_id))


class PIPPrincipaisInvestigadosView(
        JWTAuthMixin, CacheMixin, PaginatorMixin, APIView):
    cache_config = "PIP_PRINCIPAIS_INVESTIGADOS_CACHE_TIMEOUT"
    PRINCIPAIS_INVESTIGADOS_SIZE = 20

    def get(self, request, *args, **kwargs):
        orgao_id = kwargs.get("orgao_id")
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
        orgao_id = kwargs.get("orgao_id")
        cpf = kwargs.get("cpf")

        # TODO: Verificar que o post foi feito pelo mesmo orgao
        action = request.POST.get("action")
        nm_personagem = request.POST.get("nm_personagem")

        # Nome de personagem é necessário para a chave do HBase
        if not nm_personagem:
            raise ValueError("Campo 'nm_personagem' não foi dado!")
        if not action:
            raise ValueError("Campo 'action' não foi dado!")

        data = PIPPrincipaisInvestigadosDAO.save_hbase_flags(
            orgao_id, cpf, nm_personagem, action)

        return Response(data)

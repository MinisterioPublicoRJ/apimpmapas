from functools import lru_cache
from ast import literal_eval

from django.conf import settings
from django.http import Http404
from rest_framework.response import Response
from rest_framework.views import APIView

from dominio.db_connectors import run_query, HBaseGate
from dominio.mixins import CacheMixin, JWTAuthMixin
from dominio.models import Vista, Documento
from .serializers import PIPDetalheAproveitamentosSerializer
from dominio.utils import get_top_n_orderby_value_as_dict, get_value_given_key
from dominio.pip.dao import PIPRadarPerformanceDAO
from .utils import get_top_n_by_aisp, get_orgaos_same_aisps


class PIPDetalheAproveitamentosView(JWTAuthMixin, CacheMixin, APIView):
    cache_config = "PIP_DETALHEAPROVEITAMENTOS_CACHE_TIMEOUT"

    @staticmethod
    @lru_cache()
    def get_numero_aproveitamentos_pips():
        query = """
            SELECT
                orgao_id,
                nm_orgao,
                nr_aproveitamentos_periodo_atual,
                nr_aproveitamentos_periodo_anterior,
                variacao_periodo,
                tamanho_periodo_dias
            FROM {namespace}.tb_pip_detalhe_aproveitamentos
        """.format(
            namespace=settings.TABLE_NAMESPACE
        )
        return run_query(query)

    def get(self, request, *args, **kwargs):
        orgao_id = int(self.kwargs["orgao_id"])

        data = self.get_numero_aproveitamentos_pips()

        if not data:
            raise Http404

        aisps, orgaos_same_aisps = get_orgaos_same_aisps(orgao_id)
        top_n_aisp = get_top_n_by_aisp(
            orgaos_same_aisps,
            data,
            name_position=1,
            value_position=2,
            name_fieldname="nm_promotoria",
            value_fieldname="nr_aproveitamentos_periodo",
            n=3,
        )

        nr_aproveitamentos_periodo = get_value_given_key(
            data, orgao_id, key_position=0, value_position=2
        )
        variacao_periodo = get_value_given_key(
            data, orgao_id, key_position=0, value_position=4
        )
        tamanho_periodo_dias = get_value_given_key(
            data, orgao_id, key_position=0, value_position=5
        )
        top_n_pacote = get_top_n_orderby_value_as_dict(
            data,
            name_position=1,
            value_position=2,
            name_fieldname="nm_promotoria",
            value_fieldname="nr_aproveitamentos_periodo",
            n=3,
        )

        data_obj = {
            "nr_aproveitamentos_periodo": nr_aproveitamentos_periodo,
            "variacao_periodo": variacao_periodo,
            "top_n_pacote": top_n_pacote,
            "nr_aisps": aisps,
            "top_n_aisp": top_n_aisp,
            "tamanho_periodo_dias": tamanho_periodo_dias,
        }

        data = PIPDetalheAproveitamentosSerializer(data_obj).data
        return Response(data)


class PIPVistasAbertasMensal(JWTAuthMixin, CacheMixin, APIView):
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


class PIPInvestigacoesCursoAISP(JWTAuthMixin, CacheMixin, APIView):
    cache_config = "PIP_INVESTIGACOESCURSOAISP_CACHE_TIMEOUT"

    def get(self, request, *args, **kwargs):
        orgao_id = int(kwargs.get("orgao_id"))

        _, orgaos_same_aisp = get_orgaos_same_aisps(orgao_id)

        doc_count = Documento.investigacoes.em_curso_pip_aisp(
            orgaos_same_aisp
        ).count()

        data = {"aisp_nr_investigacoes": doc_count}

        return Response(data=data)


class PIPRadarPerformanceView(JWTAuthMixin, CacheMixin, APIView):
    cache_config = "PIP_RADAR_PERFORMANCE_CACHE_TIMEOUT"

    def get(self, *args, **kwargs):
        orgao_id = int(kwargs.get("orgao_id"))
        return Response(data=PIPRadarPerformanceDAO.get(orgao_id=orgao_id))


#JWTAuthMixin, 
class PIPPrincipaisInvestigadosView(CacheMixin, APIView):
    # TODO: Possivelmente passar o HBase para um DAO
    cache_config = "PIP_PRINCIPAIS_INVESTIGADOS_CACHE_TIMEOUT"

    def get(self, *args, **kwargs):
        orgao_id = kwargs.get("orgao_id")
        cpf = kwargs.get("cpf")

        row_prefix = bytes(orgao_id + cpf, encoding='utf-8')

        hbase = HBaseGate("pip_investigados_flags")
        # TODO: Util para tratar o retorno do hbase (tirar bytes e etc)
        # data = {row[0].decode(): {x[0].decode(): x[1].decode() for x in row[1].items()} for row in hbase.scan(row_prefix=row_prefix)}
        data = {row[1][b'identificacao:nm_personagem'].decode(): 
                    {
                        'is_pinned': literal_eval(row[1][b'flags:is_pinned'].decode()),
                        'is_removed': literal_eval(row[1][b'flags:is_removed'].decode())
                    }
            for row in hbase.scan(row_prefix=row_prefix)
        }
        print(data)

        return Response(data)

    def post(self, request, *args, **kwargs):
        orgao_id = kwargs.get("orgao_id")
        cpf = kwargs.get("cpf")

        # TODO: Verificar que o post foi feito pelo mesmo orgao
        # TODO: Bug, se definir "False" pro que nao for dado, 
        # vai modificar dado que n e pra modificar. Encontrar solucao.
        is_pinned = request.POST.get("is_pinned") or "False"
        is_removed = request.POST.get("is_removed") or "True"
        nm_personagem = request.POST.get("nm_personagem")
        
        if not orgao_id or not cpf or not nm_personagem:
            # TODO: Fazer um raise apropriado depois
            return Response({'error': 'orgao_id ou cpf ou nm_personagem nao dado'})
        
        row_key = bytes(orgao_id + cpf + nm_personagem, encoding='utf-8')
        print(row_key)

        data = {
            b'flags:is_pinned': bytes(is_pinned, encoding='utf-8'),
            b'flags:is_removed': bytes(is_removed, encoding='utf-8'),
            b'identificacao:orgao_id': bytes(orgao_id, encoding='utf-8'),
            b'identificacao:cpf': bytes(cpf, encoding='utf-8'),
            b'identificacao:nm_personagem': bytes(nm_personagem, encoding='utf-8'),
        }
        print(data)

        hbase = HBaseGate("pip_investigados_flags")
        hbase.insert(row_key, data=data)

        return Response({})



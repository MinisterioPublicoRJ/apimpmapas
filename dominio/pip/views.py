from functools import lru_cache

from django.conf import settings
from django.http import Http404
from rest_framework.response import Response
from rest_framework.views import APIView

from dominio.db_connectors import run_query
from dominio.mixins import CacheMixin, JWTAuthMixin
from dominio.models import Vista
from .serializers import (
    PIPDetalheAproveitamentosSerializer,
)
from dominio.utils import (
    get_top_n_orderby_value_as_dict,
    get_value_given_key
)
from .utils import (
    get_top_n_by_aisp,
    get_orgaos_same_aisps
)


class PIPDetalheAproveitamentosView(JWTAuthMixin, CacheMixin, APIView):
    cache_config = 'PIP_DETALHEAPROVEITAMENTOS_CACHE_TIMEOUT'

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
        """.format(namespace=settings.TABLE_NAMESPACE)
        return run_query(query)

    def get(self, request, *args, **kwargs):
        orgao_id = int(self.kwargs['orgao_id'])

        data = self.get_numero_aproveitamentos_pips()

        if not data:
            raise Http404

        aisps, orgaos_same_aisps = get_orgaos_same_aisps(orgao_id)
        top_n_aisp = get_top_n_by_aisp(
            orgaos_same_aisps,
            data,
            name_position=1,
            value_position=2,
            name_fieldname='nm_promotoria',
            value_fieldname='nr_aproveitamentos_periodo',
            n=3)

        nr_aproveitamentos_periodo = get_value_given_key(
            data, orgao_id, key_position=0, value_position=2)
        variacao_periodo = get_value_given_key(
            data, orgao_id, key_position=0, value_position=4)
        tamanho_periodo_dias = get_value_given_key(
            data, orgao_id, key_position=0, value_position=5)
        top_n_pacote = get_top_n_orderby_value_as_dict(
            data,
            name_position=1,
            value_position=2,
            name_fieldname='nm_promotoria',
            value_fieldname='nr_aproveitamentos_periodo',
            n=3)

        data_obj = {
            'nr_aproveitamentos_periodo': nr_aproveitamentos_periodo,
            'variacao_periodo': variacao_periodo,
            'top_n_pacote': top_n_pacote,
            'nr_aisps': aisps,
            'top_n_aisp': top_n_aisp,
            'tamanho_periodo_dias': tamanho_periodo_dias
        }

        data = PIPDetalheAproveitamentosSerializer(data_obj).data
        return Response(data)


class PIPVistasAbertasMensal(JWTAuthMixin, CacheMixin, APIView):
    cache_config = 'PIP_VISTASABERTASMENSAL_CACHE_TIMEOUT'

    def get(self, request, *args, **kwargs):
        orgao_id = int(kwargs.get("orgao_id"))
        cpf = kwargs.get("cpf")

        aberturas = Vista.vistas.aberturas_30_dias_PIP(orgao_id, cpf)
        nr_aberturas_30_dias = aberturas.count()
        nr_investigacoes_30_dias = aberturas.filter()\
            .values('documento').distinct().count()

        data = {
            'nr_aberturas_30_dias': nr_aberturas_30_dias,
            'nr_investigacoes_30_dias': nr_investigacoes_30_dias
        }

        return Response(data=data)

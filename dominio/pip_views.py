from collections import defaultdict

from django.conf import settings
from django.http import Http404
from rest_framework.response import Response
from rest_framework.views import APIView

from dominio import suamesa
from .db_connectors import run_query
from .mixins import CacheMixin, JWTAuthMixin
from .serializers import (
    PIPDetalheAproveitamentosSerializer,
)
from .mixins import CacheMixin, JWTAuthMixin


#JWTAuthMixin, 
class PIPDetalheAproveitamentosView(CacheMixin, APIView):
    cache_config = 'PIP_DETALHEAPROVEITAMENTOS_CACHE_TIMEOUT'

    @staticmethod
    def get_numero_aproveitamentos_pips():
        query = """
            SELECT
                orgao_id,
                nm_orgao,
                nr_aproveitamentos_ultimos_30_dias,
                nr_aproveitamentos_ultimos_60_dias,
                variacao_1_mes
            FROM {namespace}.tb_pip_detalhe_aproveitamentos
        """.format(namespace=settings.TABLE_NAMESPACE)
        return run_query(query)

    @staticmethod
    def get_value_from_orgao(l, orgao_id, key_position=0, value_position=2):
        for element in l:
            # orgao_id comes in position 0 of each element
            if element[key_position] == orgao_id:
                return element[value_position]
        return None

    @staticmethod
    def get_top_n_orgaos(l, orderby_position=4, n=3):
        print(l)
        sorted_list = sorted(l, key=lambda el: el[orderby_position], reverse=True)
        result_list = [
            {
                'nm_promotoria': suamesa.format_text(el[1]),
                'nr_aproveitamentos_30_dias': el[orderby_position]
            }
            for el in sorted_list
        ]
        return result_list[:n]

    @staticmethod
    def get_orgaos_same_aisps(orgao_id):
        query = "SELECT * FROM {namespace}.tb_pip_aisp".format(
            namespace=settings.TABLE_NAMESPACE)
        data = run_query(query)

        orgao_aisps = [el[1] for el in data if el[0] == orgao_id]

        aisp_list = defaultdict(list)

        for el in data:
            if el[1] in orgao_aisps:
                aisp_list[el[1]].append(el[0])

        return [{'nr_aisp': x[0], 'orgaos': x[1]} for x in sorted(aisp_list.items())]

    def get_top_n_by_aisp(self, orgaos_same_aisps, data):
        mapping_orgao_to_data = {el[0]:el for el in data}

        return [
            {'nr_aisp': aisp['nr_aisp'], 
            'top_n': self.get_top_n_orgaos(
                [mapping_orgao_to_data[orgao] for orgao in aisp['orgaos']]) 
            } 
        for aisp in orgaos_same_aisps]

    def get(self, request, *args, **kwargs):
        orgao_id = int(self.kwargs['orgao_id'])

        data = self.get_numero_aproveitamentos_pips(
            orgao_id=orgao_id
        )

        if not data:
            raise Http404
        
        orgaos_same_aisps = self.get_orgaos_same_aisps(orgao_id)
        top_n_by_aisp = self.get_top_n_by_aisp(orgaos_same_aisps, data)

        nr_aproveitamentos_ultimos_30_dias = self.get_value_from_orgao(
            data, orgao_id, value_position=2)
        variacao_1_mes = self.get_value_from_orgao(
            data, orgao_id, value_position=4)
        top_n_pacote = self.get_top_n_orgaos(data, n=3)

        data_obj = {
            'nr_aproveitamentos_30_dias': nr_aproveitamentos_ultimos_30_dias,
            'variacao_1_mes': variacao_1_mes,
            'top_n_pacote': top_n_pacote,
            'top_n_by_aisp': top_n_by_aisp
        }

        data = PIPDetalheAproveitamentosSerializer(data_obj).data
        return Response(data)

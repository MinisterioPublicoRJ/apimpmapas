from django.db import connections
from django.http import Http404
from rest_framework.response import Response
from rest_framework.views import APIView

from dominio.tutela import suamesa
from dominio.mixins import CacheMixin, PaginatorMixin, JWTAuthMixin
from dominio.models import Vista
from dominio.tutela.serializers import (
    SuaMesaListaVistasSerializer,
)
from dominio.tutela.dao import (
    OutliersDAO,
    SaidasDAO,
    EntradasDAO,
    RadarPerformanceDAO,
    ComparadorRadaresDAO,
    TempoTramitacaoIntegradoDAO,
    TempoTramitacaoDAO,
    ListaProcessosDAO,
    ListaInvestigacoesDAO,
)


class OutliersView(JWTAuthMixin, CacheMixin, APIView):
    cache_config = 'OUTLIERS_CACHE_TIMEOUT'

    def get(self, request, *args, **kwargs):
        orgao_id = int(self.kwargs.get(self.orgao_url_kwarg))
        data = OutliersDAO.get(orgao_id=orgao_id)

        return Response(data)


class SaidasView(JWTAuthMixin, CacheMixin, APIView):
    cache_config = 'SAIDAS_CACHE_TIMEOUT'

    def get(self, request, *args, **kwargs):
        orgao_id = int(self.kwargs.get(self.orgao_url_kwarg))
        data = SaidasDAO.get(orgao_id=orgao_id)

        return Response(data)


class EntradasView(JWTAuthMixin, CacheMixin, APIView):
    cache_config = 'ENTRADAS_CACHE_TIMEOUT'

    def get(self, request, *args, **kwargs):
        orgao_id = int(self.kwargs.get(self.orgao_url_kwarg))
        nr_cpf = str(self.kwargs['nr_cpf'])
        data = EntradasDAO.get(orgao_id=orgao_id, nr_cpf=nr_cpf)

        return Response(data)


class SuaMesaDetalheView(JWTAuthMixin, CacheMixin, APIView):
    cache_config = 'SUAMESADETALHE_CACHE_TIMEOUT'

    def get(self, request, *args, **kwargs):
        orgao_id = int(kwargs.get(self.orgao_url_kwarg))
        cpf = kwargs.get("cpf")

        mesa_detalhe = Vista.vistas.agg_abertas_por_data(orgao_id, cpf)
        if all([v is None for v in mesa_detalhe.values()]):
            raise Http404

        return Response(mesa_detalhe)


class SuaMesaVistasListaView(
        JWTAuthMixin, CacheMixin, PaginatorMixin, APIView):
    cache_config = 'SUAMESAVISTASLISTA_CACHE_TIMEOUT'

    def get(self, request, *args, **kwargs):
        orgao_id = int(kwargs.get(self.orgao_url_kwarg))
        cpf = kwargs.get("cpf")
        abertura = kwargs.get("abertura")
        lista_aberturas = ("ate_vinte", "vinte_trinta", "trinta_mais")
        page = int(request.GET.get("page", 1))

        if abertura not in lista_aberturas:
            msg = "data_abertura inválida. "\
                  f"Opções são: {', '.join(lista_aberturas)}"
            return Response(data=msg, status=404)
        data = Vista.vistas.abertas_por_data(orgao_id, cpf, abertura)
        page_data = self.paginate(
            data,
            page=page,
            page_size=suamesa.VISTAS_PAGE_SIZE
        )
        vistas_lista = SuaMesaListaVistasSerializer(page_data, many=True).data

        return Response(data=vistas_lista)


class TempoTramitacaoView(JWTAuthMixin, CacheMixin, APIView):
    cache_config = 'TEMPO_TRAMITACAO_CACHE_TIMEOUT'

    def get(self, request, *args, **kwargs):
        orgao_id = int(self.kwargs.get(self.orgao_url_kwarg))
        version = self.request.GET.get('version')

        if version == '1.1':
            DAO = TempoTramitacaoIntegradoDAO
        else:
            DAO = TempoTramitacaoDAO

        data = DAO.get(orgao_id=orgao_id)

        return Response(data)


class DesarquivamentosView(JWTAuthMixin, CacheMixin, APIView):
    cache_config = "DESARQUIVAMENTOS_CACHE_TIMEOUT"
    fields = ["numero_mprj", "qtd_desarq"]

    def fetch_set(self, cursor):
        return [dict(zip(self.fields, row)) for row in cursor.fetchall()]

    def get_data(self, orgao_id):
        with connections["dominio_db"].cursor() as cursor:
            query = """
                WITH AGRUPADOS AS (SELECT d.docu_nr_mp, COUNT(d.docu_nr_mp)
                FROM MCPR_DOCUMENTO d
                JOIN mcpr_vista v ON v.vist_docu_dk = d.docu_dk
                JOIN mcpr_andamento a ON a.pcao_vist_dk = v.vist_dk
                JOIN mcpr_sub_andamento sa ON sa.stao_pcao_dk = a.pcao_dk
                JOIN mcpr_tp_andamento ta ON ta.tppr_dk = sa.stao_tppr_dk
                WHERE sa.stao_tppr_dk IN (6075, 1028, 6798, 7245, 6307, 1027,
                                          7803, 6003, 7802, 7801)
                                          AND d.docu_cldc_dk = 392
                AND d.DOCU_ORGI_ORGA_DK_RESPONSAVEL = %s
                AND d.DOCU_TPST_DK != 11
                AND a.pcao_dt_cancelamento IS NULL
                GROUP BY docu_nr_mp, a.pcao_dt_andamento)
                SELECT docu_nr_mp, COUNT(docu_nr_mp)
                FROM AGRUPADOS GROUP BY docu_nr_mp
            """
            result_set = cursor.execute(query, [orgao_id])
            return self.fetch_set(result_set)

    def get(self, request, *args, **kwargs):
        orgao_id = int(self.kwargs.get(self.orgao_url_kwarg))
        # TODO: pensar numa forma geral de discernir 404 de respostas
        # vazias e respostas não existentes

        return Response(data=self.get_data(orgao_id))


class ListaProcessosView(JWTAuthMixin, CacheMixin, PaginatorMixin, APIView):
    cache_config = 'LISTA_PROCESSOS_CACHE_TIMEOUT'
    PAGE_SIZE = 20

    def get(self, request, *args, **kwargs):
        orgao_id = int(self.kwargs.get(self.orgao_url_kwarg))
        page = int(request.GET.get("page", 1))

        data = ListaProcessosDAO.get(orgao_id=orgao_id)

        page_data = self.paginate(
            data,
            page=page,
            page_size=self.PAGE_SIZE
        )
        response = {
            'procedimentos': page_data,
            'nr_paginas': self.get_n_pages(data)
        }

        return Response(data=response)


class ListaInvestigacoesView(
        JWTAuthMixin, CacheMixin, PaginatorMixin, APIView):
    cache_config = 'LISTA_INVESTIGACOES_CACHE_TIMEOUT'
    PAGE_SIZE = 20

    def get(self, request, *args, **kwargs):
        orgao_id = int(self.kwargs.get(self.orgao_url_kwarg))
        page = int(request.GET.get("page", 1))

        data = ListaInvestigacoesDAO.get(orgao_id=orgao_id)

        page_data = self.paginate(
            data,
            page=page,
            page_size=self.PAGE_SIZE
        )
        response = {
            'procedimentos': page_data,
            'nr_paginas': self.get_n_pages(data)
        }

        return Response(data=response)


class RadarView(JWTAuthMixin, CacheMixin, APIView):
    cache_config = 'RADAR_CACHE_TIMEOUT'

    def parse_orgao_id(self, orgao_id):
        try:
            orgao_id = int(orgao_id)
        except ValueError:
            raise Http404("Valor <orgao_id> inválido")

        return orgao_id

    def get(self, request, *args, **kwargs):
        orgao_id = self.parse_orgao_id(kwargs.get("orgao_id"))

        data = RadarPerformanceDAO.get(orgao_id=orgao_id)
        return Response(data=data)


class ComparadorRadaresView(JWTAuthMixin, APIView):
    def get(self, request, *args, **kwargs):
        orgao_id = int(self.kwargs.get(self.orgao_url_kwarg))
        return Response(data=ComparadorRadaresDAO.get(orgao_id=orgao_id))

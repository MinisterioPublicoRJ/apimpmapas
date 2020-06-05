"""
Definição do DAO (Data Access Object) usado pela View do SuaMesa.

Este DAO irá pegar o tipo de dado a ser buscado (especificado no request),
e irá chamar a função apropriada para fazer esta busca.

Caso o tipo de dado não seja especificado, ou seja informado um tipo de dado
não definido, o DAO irá levantar uma exceção.
"""

from django.conf import settings

from dominio.suamesa.exceptions import (
    APIInvalidSuaMesaType,
    APIMissingSuaMesaType,
)
from dominio.suamesa import dao_functions
from dominio.suamesa.serializers import SuaMesaDetalheCPFSerializer, SuaMesaDetalheTopNSerializer, SuaMesaDetalheOrgaoSerializer, SuaMesaDetalheAISPSerializer
from dominio.dao import GenericDAO
from dominio.db_connectors import execute as impala_execute
from dominio.pip.utils import get_orgaos_same_aisps


class SuaMesaDAO:
    _type_switcher = {
        'vistas': dao_functions.get_vistas,
        'tutela_investigacoes': dao_functions.get_tutela_investigacoes,
        'tutela_processos': dao_functions.get_tutela_processos,
        'pip_inqueritos': dao_functions.get_pip_inqueritos,
        'pip_pics': dao_functions.get_pip_pics,
        'pip_aisp': dao_functions.get_pip_aisp,
        'tutela_finalizados': dao_functions.get_tutela_finalizados,
        'pip_finalizados': dao_functions.get_pip_finalizados
    }

    @classmethod
    def get(cls, orgao_id, request):
        tipo = request.GET.get("tipo")

        if not tipo:
            raise APIMissingSuaMesaType

        get_data = cls.switcher(tipo)
        return {'nr_documentos': get_data(orgao_id, request)}

    @classmethod
    def switcher(cls, tipo):
        if tipo not in cls._type_switcher:
            raise APIInvalidSuaMesaType
        return cls._type_switcher[tipo]


class SuaMesaDetalheOrgaoDAO(GenericDAO):
    QUERIES_DIR = settings.BASE_DIR.child("dominio", "suamesa", "queries")
    query_file = "detalhe_documento_orgao.sql"
    columns = [
        'tipo_detalhe',
        'intervalo',
        'nm_orgao',
        'cod_pacote',
        'orgao_id',
        'nr_documentos_distintos_atual',
        'nr_aberturas_vista_atual',
        'nr_aproveitamentos_atual',
        'nr_instaurados_atual',
        'acervo_anterior',
        'acervo_atual',
        'variacao_acervo',
        'nr_documentos_distintos_anterior',
        'nr_aberturas_vista_anterior',
        'nr_aproveitamentos_anterior',
        'nr_instaurados_anterior',
        'variacao_documentos_distintos',
        'variacao_aberturas_vista',
        'variacao_aproveitamentos',
        'variacao_instaurados'
    ]
    serializer = SuaMesaDetalheOrgaoSerializer
    table_namespaces = {"schema": settings.TABLE_NAMESPACE}

    @classmethod
    def get(cls, orgao_id, request, accept_empty=True):
        kwargs = {
            'orgao_id': orgao_id,
            'tipo_detalhe': request.GET.get('tipo'),
        }

        return super().get(accept_empty, **kwargs)


class SuaMesaDetalheCPFDAO(GenericDAO):
    QUERIES_DIR = settings.BASE_DIR.child("dominio", "suamesa", "queries")
    query_file = "detalhe_documento_orgao_cpf.sql"
    columns = [
        'tipo_detalhe',
        'intervalo',
        'orgao_id',
        'cpf',
        'nr_documentos_distintos_atual',
        'nr_aberturas_vista_atual',
        'nr_aproveitamentos_atual',
        'nr_instaurados_atual',
        'nr_documentos_distintos_anterior',
        'nr_aberturas_vista_anterior',
        'nr_aproveitamentos_anterior',
        'nr_instaurados_anterior',
        'variacao_documentos_distintos',
        'variacao_aberturas_vista',
        'variacao_aproveitamentos',
        'variacao_instaurados'
    ]
    serializer = SuaMesaDetalheCPFSerializer
    table_namespaces = {"schema": settings.TABLE_NAMESPACE}

    @classmethod
    def get(cls, orgao_id, request, accept_empty=True):
        kwargs = {
            'orgao_id': orgao_id,
            'tipo_detalhe': request.GET.get('tipo'),
            'cpf': request.GET.get('cpf'),
        }

        return super().get(accept_empty, **kwargs)


class SuaMesaDetalheTopNDAO(GenericDAO):
    QUERIES_DIR = settings.BASE_DIR.child("dominio", "suamesa", "queries")
    query_file = "top_n_documento_orgao.sql"
    columns = [
        'nm_orgao',
        'valor',
    ]
    serializer = SuaMesaDetalheTopNSerializer
    table_namespaces = {
        "schema": settings.TABLE_NAMESPACE,
        "nm_campo": "{nm_campo}",
    }

    def __init__(self, ranking_fieldname):
        self.ranking_fieldname = ranking_fieldname

    def execute(self, **kwargs):
        return impala_execute(super().query().format(nm_campo=self.ranking_fieldname), kwargs)

    def get(self, accept_empty=False, **kwargs):
        result_set = self.execute(**kwargs)
        if not result_set and not accept_empty:
            raise APIEmptyResultError

        return super().serialize(result_set)


class SuaMesaDetalheTopNAISPDAO(SuaMesaDetalheTopNDAO):
    query_file = "top_n_documento_aisp.sql"


class SuaMesaDetalheAggMixin:
    ranking_fields = []
    ranking_dao = SuaMesaDetalheTopNDAO

    @classmethod
    def get_metrics_data(cls, orgao, request, accept_empty=True):
        data = super().get(orgao, request, accept_empty=accept_empty)
        data = data[0] if data else {}
        return data

    @classmethod
    def get_ranking_data(cls, orgao, request, accept_empty=True):
        kwargs = {
            'orgao_id': orgao,
            'tipo_detalhe': request.GET.get('tipo'),
            'n': request.GET.get('n', 3)
        }

        data = []

        for fieldname in cls.ranking_fields:
            ranking_dao = cls.ranking_dao(fieldname)
            response = ranking_dao.get(accept_empty=True, **kwargs)
            if response:
                data.append({'ranking_fieldname': fieldname, 'data': response})
        
        return data

    @classmethod
    def get(cls, orgao, request):
        metrics_data = cls.get_metrics_data(orgao, request)
        ranking_data = cls.get_ranking_data(orgao, request)

        if not metrics_data and not ranking_data:
            cls.raise_empty_result_error()

        result = {
            'metrics': metrics_data,
            'rankings': ranking_data,
            'mapData': {},
        }

        return result


class SuaMesaDetalhePIPInqueritoDAO(SuaMesaDetalheAggMixin, SuaMesaDetalheCPFDAO):
    ranking_fields = ['variacao_documentos_distintos']


class SuaMesaDetalhePIPPICSDAO(SuaMesaDetalheAggMixin, SuaMesaDetalheCPFDAO):
    ranking_fields = ['nr_documentos_distintos_atual', 'nr_aproveitamentos_atual']


class SuaMesaDetalhePIPAISPDAO(SuaMesaDetalheAggMixin, SuaMesaDetalheOrgaoDAO):
    query_file = "detalhe_documento_aisp.sql"
    columns = [
        'acervo_inicio',
        'acervo_fim',
        'variacao_acervo',
        'aisp_nomes'
    ]
    serializer = SuaMesaDetalheAISPSerializer


class SuaMesaDetalheTutelaInvestigacoesDAO(SuaMesaDetalheAggMixin, SuaMesaDetalheOrgaoDAO):
    ranking_fields = ['variacao_acervo']


class SuaMesaDetalheFactoryDAO(SuaMesaDAO):
    _type_switcher = {
        'pip_inqueritos': SuaMesaDetalhePIPInqueritoDAO,
        'pip_pics': SuaMesaDetalhePIPPICSDAO,
        'pip_aisp': SuaMesaDetalhePIPAISPDAO,
        'tutela_investigacoes': SuaMesaDetalheTutelaInvestigacoesDAO,
    }

    @classmethod
    def get(cls, orgao_id, request):
        tipo = request.GET.get("tipo")

        if not tipo:
            raise APIMissingSuaMesaType

        DAO = cls.switcher(tipo)
        return DAO.get(orgao_id, request)

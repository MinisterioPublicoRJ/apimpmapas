"""
Definição do DAO (Data Access Object) usado pela View do SuaMesa.

Este DAO irá pegar o tipo de dado a ser buscado (especificado no request),
e irá chamar a função apropriada para fazer esta busca.

Caso o tipo de dado não seja especificado, ou seja informado um tipo de dado
não definido, o DAO irá levantar uma exceção.
"""

from dominio.suamesa.exceptions import (
    APIInvalidSuaMesaType,
    APIMissingSuaMesaType,
)
from dominio.suamesa import dao_functions
from dominio.suamesa.serializers import (
    SuaMesaDetalheAISPSerializer,
    SuaMesaDetalheTutelaProcessosSerializer,
)
from dominio.suamesa.dao_rankings import (
    RankingDAO,
    RankingMixin,
    RankingPercentageMixin,
)
from dominio.suamesa.dao_metrics import (
    MetricsDataObjectDAO,
    MetricsDetalheDocumentoOrgaoDAO,
    MetricsDetalheDocumentoOrgaoCPFDAO,
)


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


class SuaMesaDetalhePIPInqueritosDAO(
        RankingMixin, MetricsDetalheDocumentoOrgaoCPFDAO):
    ranking_fields = [
        'nr_documentos_distintos_atual',
        'nr_aproveitamentos_atual',
    ]


class SuaMesaDetalhePIPPICSDAO(
       RankingMixin, MetricsDetalheDocumentoOrgaoCPFDAO):
    ranking_fields = [
        'acervo_fim',
        'nr_instaurados_atual'
    ]


class SuaMesaDetalhePIPAISPDAO(RankingMixin, MetricsDetalheDocumentoOrgaoDAO):
    class RankingAISPDAO(RankingDAO):
        query_file = "ranking_documento_aisp.sql"

    query_file = "detalhe_documento_aisp.sql"
    columns = [
        'acervo_inicio',
        'acervo_fim',
        'variacao_acervo',
        'aisp_nomes'
    ]
    serializer = SuaMesaDetalheAISPSerializer
    ranking_fields = ['acervo_fim']
    ranking_dao = RankingAISPDAO


class SuaMesaDetalheTutelaInvestigacoesDAO(
        RankingPercentageMixin, MetricsDetalheDocumentoOrgaoDAO):
    ranking_fields = ['variacao_acervo']


class SuaMesaDetalheTutelaProcessosDAO(RankingMixin, MetricsDataObjectDAO):
    class RankingTutelaProcessosDAO(RankingDAO):
        query_file = "ranking_tutela_processo.sql"

    query_file = "detalhe_tutela_processo.sql"
    columns = [
        'orgao_id',
        'nm_orgao',
        'nr_acoes_ultimos_60_dias',
        'variacao_12_meses',
        'nr_acoes_ultimos_30_dias',
    ]
    serializer = SuaMesaDetalheTutelaProcessosSerializer
    ranking_fields = ['nr_acoes_ultimos_30_dias']
    ranking_dao = RankingTutelaProcessosDAO


class SuaMesaDetalheFactoryDAO(SuaMesaDAO):
    _type_switcher = {
        'pip_inqueritos': SuaMesaDetalhePIPInqueritosDAO,
        'pip_pics': SuaMesaDetalhePIPPICSDAO,
        'pip_aisp': SuaMesaDetalhePIPAISPDAO,
        'tutela_investigacoes': SuaMesaDetalheTutelaInvestigacoesDAO,
        'tutela_processos': SuaMesaDetalheTutelaProcessosDAO,
    }

    @classmethod
    def get(cls, orgao_id, request):
        tipo = request.GET.get("tipo")

        if not tipo:
            raise APIMissingSuaMesaType

        DAO = cls.switcher(tipo)
        return DAO.get(orgao_id=orgao_id, request=request)


class DocumentoDAO:
    pass

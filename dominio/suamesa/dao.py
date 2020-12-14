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
    RankingPercentageDAO,
    RankingMixin,
    RankingPercentageMixin,
)
from dominio.suamesa.dao_metrics import (
    MetricsDataObjectDAO,
    MetricsDetalheDocumentoOrgaoDAO,
    MetricsDetalheDocumentoOrgaoCPFDAO,
)
from dominio.pip.utils import get_orgaos_same_aisps
from dominio.db_connectors import execute as impala_execute


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
        'variacao_acervo'
    ]
    serializer = SuaMesaDetalheAISPSerializer
    ranking_fields = ['acervo_fim']
    ranking_dao = RankingAISPDAO

    @classmethod
    def execute(cls, **kwargs):
        orgao_id = kwargs['orgao_id']
        _, orgaos = get_orgaos_same_aisps(orgao_id)

        data = {f"orgao_aisp_{i}": v for i, v in enumerate(orgaos)}
        kwargs.update(data)

        params = ",".join([f":{k}" for k in data.keys()])
        query = cls.query().replace(":orgaos_aisp", params)

        return impala_execute(query, kwargs)


class SuaMesaDetalheTutelaInvestigacoesDAO(
        RankingPercentageMixin, MetricsDetalheDocumentoOrgaoDAO):
    class RankingTutelaInvestigacoesAumentosDAO(RankingPercentageDAO):
        query_file = "ranking_investigacoes_aumentos.sql"

    class RankingTutelaInvestigacoesReducoesDAO(RankingPercentageDAO):
        query_file = "ranking_investigacoes_reducoes.sql"

    ranking_fields = ['aumento_acervo', 'reducao_acervo']
    ranking_dao = [
        RankingTutelaInvestigacoesAumentosDAO,
        RankingTutelaInvestigacoesReducoesDAO
    ]


class SuaMesaDetalheTutelaProcessosDAO(RankingMixin, MetricsDataObjectDAO):
    class RankingTutelaProcessosDAO(RankingDAO):
        query_file = "ranking_tutela_processo.sql"

    query_file = "detalhe_tutela_processo.sql"
    columns = [
        'orgao_id',
        'nm_orgao',
        'nr_acoes_12_meses_anterior',
        'nr_acoes_12_meses_atual',
        'variacao_12_meses',
        'nr_acoes_60_dias_anterior',
        'nr_acoes_ultimos_60_dias',
        'variacao_60_dias',
        'nr_acoes_30_dias_anterior',
        'nr_acoes_ultimos_30_dias',
        'variacao_30_dias'
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

        kwargs = {
            'orgao_id': orgao_id,
            'tipo_detalhe': tipo,
            'cpf': request.GET.get('cpf'),
            'n': int(request.GET.get('n', 3)),
            'intervalo': request.GET.get('intervalo', 'mes')
        }

        DAO = cls.switcher(tipo)
        return DAO.get(**kwargs)

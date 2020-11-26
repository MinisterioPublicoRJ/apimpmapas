from django.conf import settings
from django.core.cache import cache

from dominio.dao import GenericDAO, SingleDataObjectDAO
from dominio.db_connectors import get_hbase_table, run_query
from dominio.alertas import serializers
from dominio.alertas.helper import ordem as alrt_ordem
from dominio.alertas.exceptions import (
    APIInvalidOverlayType,
    APIMissingOverlayType,
)


class FiltraAlertasDispensadosMixin:
    orgao_kwarg = None
    alerta_id_kwarg = None
    sigla_kwarg = None
    col_family = "dados_alertas:"

    @classmethod
    def prepara_hbase_query(cls, orgao_id):
        return (
            "SingleColumnValueFilter('dados_alertas', 'orgao', =,"
            f" 'binary:{orgao_id}')"
            " OR SingleColumnValueFilter('dados_alertas', 'orgao', =,"
            " 'binary:ALL')"
        ).encode()

    @classmethod
    def prepara_dados_hbase(cls, dados):
        sigla_key = f"{cls.col_family}sigla".encode()
        id_key = f"{cls.col_family}alerta_id".encode()
        prep_dados = []
        for _, dado in dados:
            prep_dados.append(
                (dado[sigla_key].decode(), dado[id_key].decode())
            )

        return prep_dados

    @classmethod
    def get_table(cls):
        return get_hbase_table(
            settings.PROMOTRON_HBASE_NAMESPACE
            + settings.HBASE_DISPENSAR_ALERTAS_TABLE
        )

    @classmethod
    def filtra(cls, orgao_id, result_set):
        table = cls.get_table()
        dispensados = cls.prepara_dados_hbase(
            table.scan(filter=cls.prepara_hbase_query(orgao_id))
        )

        filtrados = []
        for row in result_set:
            if (row[cls.sigla_kwarg], row[cls.alerta_id_kwarg]) in dispensados:
                continue

            filtrados.append(row)

        return filtrados

    @classmethod
    def get(cls, accept_empty=False, **kwargs):
        orgao_id = kwargs.get(cls.orgao_kwarg)
        result_set = super().get(accept_empty=accept_empty, **kwargs)
        return cls.filtra(orgao_id, result_set)


class AlertasDAO(GenericDAO):
    QUERIES_DIR = settings.BASE_DIR.child("dominio", "alertas", "queries")

    @classmethod
    def ordena_alertas(cls, alertas):
        ordem_dict = {s: i for i, s in enumerate(alrt_ordem)}
        alertas = [x for x in alertas if x["sigla"] in ordem_dict]
        return sorted(alertas, key=lambda x: ordem_dict[x["sigla"]])


class AlertaMaxPartitionDAO(AlertasDAO):
    query_file = "alerta_max_dt_partition.sql"
    table_namespaces = {
        "schema": settings.TABLE_NAMESPACE,
    }
    cache_prefix = 'ALERTA_MAX_DT_PARTITION'

    @classmethod
    def get(cls):
        data = cache.get(cls.cache_prefix, default=None)
        if not data:
            data = cls.execute()
            if not data:
                return '-1'
            data = data[0][0]
            cache.set(cls.cache_prefix, data, timeout=settings.CACHE_TIMEOUT)
        return data


class ResumoAlertasDAO(AlertasDAO):
    """
    Classe principal do Resumo dos Alertas.
    Esta classe executa todos os outros DAOs de resumo de alertas
    que herdam dela.
    """

    query_file = "resumo_alertas.sql"
    columns = ["sigla", "count"]
    table_namespaces = {
        "schema": settings.TABLE_NAMESPACE,
        "schema_alertas_compras": settings.SCHEMA_ALERTAS,
    }
    serializer = serializers.AlertasResumoSerializer

    @classmethod
    def get_all(cls, id_orgao):
        dt_partition = AlertaMaxPartitionDAO.get()
        resumo = super().get(
            id_orgao=id_orgao,
            dt_partition=dt_partition,
            accept_empty=True
        )

        return cls.ordena_alertas(resumo)


class AlertaMGPDAO(AlertasDAO):
    query_file = None
    table_namespaces = {"schema": settings.TABLE_NAMESPACE}
    columns = [
        "doc_dk",
        "num_doc",
        "data_alerta",
        "orgao",
        "dias_passados",
        "id_alerta",
        "sigla",
        "descricao",
        "classe_hierarquia"
    ]

    @classmethod
    def execute(cls, **kwargs):
        return run_query(cls.query(), kwargs) or []

    @classmethod
    def get(cls, accept_empty=True, **kwargs):
        if kwargs.get("tipo_alerta") is not None:
            cls.query_file = "validos_por_orgao_tipo.sql"
        else:
            cls.query_file = "validos_por_orgao_base.sql"

        kwargs['dt_partition'] = AlertaMaxPartitionDAO.get()
        result_set = super().get(accept_empty=accept_empty, **kwargs)
        return cls.ordena_alertas(result_set)


class AlertaComprasDAO(FiltraAlertasDispensadosMixin, AlertasDAO):
    query_file = "alerta_compras.sql"
    columns = ["sigla", "contrato", "iditem", "contrato_iditem", "item"]
    serializer = serializers.AlertasComprasSerializer
    table_namespaces = {
        "schema": settings.TABLE_NAMESPACE,
        "schema_alertas_compras": settings.SCHEMA_ALERTAS,
    }

    orgao_kwarg = "id_orgao"
    alerta_id_kwarg = "contrato_iditem"
    sigla_kwarg = "sigla"


# ------ DAOs relativos ao Overlay do Alerta

class AlertaOverlayPrescricaoDAO(AlertasDAO):
    query_file = "alerta_overlay_prescricao.sql"
    columns = [
        'tipo_penal',
        'nm_investigado',
        'max_pena',
        'delitos_multiplicadores',
        'fator_pena',
        'max_pena_fatorado',
        'dt_inicio_prescricao',
        'dt_fim_prescricao',
        'adpr_chave'
    ]
    serializer = serializers.AlertaOverlayPrescricaoSerializer
    table_namespaces = {
        "schema_exadata": settings.EXADATA_NAMESPACE,
        "schema": settings.TABLE_NAMESPACE
    }


class AlertaOverlayIC1ADAO(AlertasDAO, SingleDataObjectDAO):
    query_file = "alerta_overlay_ic1a.sql"
    columns = [
        'dt_fim_prazo',
        'dt_movimento',
        'desc_movimento'
    ]
    table_namespaces = {
        "schema": settings.TABLE_NAMESPACE
    }


class AlertaOverlayPA1ADAO(AlertasDAO, SingleDataObjectDAO):
    query_file = "alerta_overlay_pa1a.sql"
    columns = [
        'dt_fim_prazo',
        'docu_dt_cadastro'
    ]
    table_namespaces = {
        "schema_exadata": settings.EXADATA_NAMESPACE,
        "schema": settings.TABLE_NAMESPACE
    }


class AlertaOverlayPPFPDAO(AlertasDAO, SingleDataObjectDAO):
    query_file = "alerta_overlay_ppfp.sql"
    columns = [
        'docu_dt_cadastro'
    ]
    table_namespaces = {
        "schema_exadata": settings.EXADATA_NAMESPACE
    }


class AlertasOverlayDAO:
    _type_switcher = {
        'prescricao': AlertaOverlayPrescricaoDAO,
        'pa1a': AlertaOverlayPA1ADAO,
        'ic1a': AlertaOverlayIC1ADAO,
        'ppfp': AlertaOverlayPPFPDAO
    }

    @classmethod
    def get(cls, docu_dk, request):
        tipo = request.GET.get("tipo")
        if not tipo:
            raise APIMissingOverlayType

        DAO = cls.switcher(tipo)

        dt_partition = AlertaMaxPartitionDAO.get()
        return DAO.get(
            docu_dk=docu_dk,
            dt_partition=dt_partition
        )

    @classmethod
    def switcher(cls, tipo):
        if tipo not in cls._type_switcher:
            raise APIInvalidOverlayType
        return cls._type_switcher[tipo]


class DetalheAlertaCompraDAO(SingleDataObjectDAO):
    QUERIES_DIR = settings.BASE_DIR.child("dominio", "alertas", "queries")
    serializer = serializers.DetalheAlertaSerializer

    query_file = "detalhe_alerta_compra.sql"
    columns = [
        "contratacao",
        "data_contratacao",
        "item_contratado",
        "var_perc",
    ]
    table_namespaces = {
        "schema_alertas_compras": settings.SCHEMA_ALERTAS,
    }

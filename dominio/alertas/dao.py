from django.conf import settings

from database.db_connect import Oracle_DB
from dominio.dao import GenericDAO
from dominio.db_connectors import get_hbase_table, run_query
from dominio.alertas import serializers
from dominio.alertas.helper import ordem as alrt_ordem


class FiltraAlertasDispensadosMixin:
    orgao_kwarg = None
    alerta_id_kwarg = None
    sigla_kwarg = None
    col_family = "dados_alertas:"

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
            table.scan(row_prefix=f"{orgao_id}".encode())
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


class ResumoAlertasDAO:
    """
    Classe principal do Resumo dos Alertas.
    Esta classe executa todos os outros DAOs de resumo de alertas
    que herdam dela.
    """

    columns = ["sigla", "descricao", "orgao", "count"]
    serializer = serializers.AlertasResumoSerializer

    @classmethod
    def get_all(cls, id_orgao):
        resumo = []
        for ResumoDAOClass in cls.__subclasses__():
            resumo.extend(
                ResumoDAOClass.get(id_orgao=id_orgao, accept_empty=True)
            )
        return cls.ordena_resumo(resumo)

    @classmethod
    def ordena_resumo(cls, resumo):
        return [
            res_alerta
            for sigla in alrt_ordem
            for res_alerta in resumo
            if res_alerta["sigla"] == sigla
        ]


class ResumoAlertasMGPDAO(ResumoAlertasDAO, AlertasDAO):
    query_file = "resumo_alertas_mgp.sql"
    table_namespaces = {"schema": settings.TABLE_NAMESPACE}


class ResumoAlertasComprasDAO(ResumoAlertasDAO, AlertasDAO):
    query_file = "resumo_alertas_compras.sql"
    table_namespaces = {
        "schema": settings.TABLE_NAMESPACE,
        "schema_alertas_compras": settings.SCHEMA_ALERTAS,
    }


class AlertaMGPDAO(AlertasDAO):
    query_file = None
    table_namespaces = {"schema": settings.TABLE_NAMESPACE}
    columns = [
        "doc_dk",
        "num_doc",
        "num_ext",
        "etiqueta",
        "classe_doc",
        "data_alerta",
        "orgao",
        "classe_hier",
        "dias_passados",
        "id_alerta",
        "descricao",
        "sigla",
    ]

    @classmethod
    def ordena_alertas(cls, alertas):
        return [
            res_alerta
            for sigla in alrt_ordem
            for res_alerta in alertas
            if res_alerta["sigla"] == sigla
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

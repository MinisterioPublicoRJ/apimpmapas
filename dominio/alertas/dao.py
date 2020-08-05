from django.conf import settings

from dominio.dao import GenericDAO
from dominio.alertas import serializers


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

        return resumo


class ResumoAlertasMGPDAO(ResumoAlertasDAO, AlertasDAO):
    query_file = "resumo_alertas_mgp.sql"
    table_namespaces = {"schema": settings.TABLE_NAMESPACE}


class ResumoAlertasComprasDAO(ResumoAlertasDAO, AlertasDAO):
    query_file = "resumo_alertas_compras.sql"
    table_namespaces = {
        "schema": settings.TABLE_NAMESPACE,
        "schema_alertas_compras": settings.SCHEMA_ALERTAS,
    }


class AlertaComprasDAO(AlertasDAO):
    query_file = "alerta_compras.sql"
    columns = [
        "sigla",
        "contrato",
        "iditem",
        "contrato_iditem",
        "item"
    ]
    serializer = serializers.AlertasComprasSerializer
    table_namespaces = {
        "schema": settings.TABLE_NAMESPACE,
        "schema_alertas_compras": settings.SCHEMA_ALERTAS,
    }

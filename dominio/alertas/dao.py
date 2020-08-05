from django.conf import settings

from dominio.dao import GenericDAO
from dominio.alertas import serializers


class AlertasDAO(GenericDAO):
    QUERIES_DIR = settings.BASE_DIR.child("dominio", "alertas", "queries")


class ResumoAlertasDAO:
    columns = ["sigla", "descricao", "orgao", "count"]
    serializer = serializers.AlertasResumoSerializer


class ResumoAlertasMGPDAO(ResumoAlertasDAO, AlertasDAO):
    query_file = "resumo_alertas_mgp.sql"
    table_namespaces = {"schema": settings.TABLE_NAMESPACE}


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

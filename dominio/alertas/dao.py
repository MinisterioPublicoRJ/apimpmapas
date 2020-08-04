from django.conf import settings

from dominio.dao import GenericDAO
from dominio.alertas.serializers import AlertasComprasSerializer


class AlertaComprasDAO(GenericDAO):
    QUERIES_DIR = settings.BASE_DIR.child("dominio", "alertas", "queries")
    query_file = "alerta_compras.sql"
    columns = [
        "sigla",
        "contrato",
        "iditem",
        "contrato_iditem",
        "item"
    ]
    serializer = AlertasComprasSerializer
    table_namespaces = {
        "schema": settings.TABLE_NAMESPACE,
        "schema_alertas_compras": settings.SCHEMA_ALERTAS,
    }

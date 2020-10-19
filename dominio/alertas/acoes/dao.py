from django.conf import settings

from dominio.dao import GenericDAO


class ListaROsAusentesDAO(GenericDAO):
    QUERIES_DIR = settings.BASE_DIR.child(
        "dominio", "alertas", "acoes", "queries"
    )
    query_file = "lista_ros_ausentes.sql"
    columns = ["proc_numero_serial"]
    table_namespaces = {
        "schema_opengeo": settings.SCHEMA_OPENGEO_BDA
    }

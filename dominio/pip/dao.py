from django.conf import settings

from dominio.db_connectors import execute as impala_execute


QUERIES_DIR = settings.BASE_DIR.child("dominio", "pip", "queries")


class PIPIndicadoresSucessoDAO:
    query_file = "pip_taxa_resolutividade.sql"
    column = "taxa_resolutivdade"

    @classmethod
    def serialize(cls, result_set):
        return {cls.column: result_set[0]}

    @classmethod
    def execute(cls, **kwargs):
        with open(QUERIES_DIR.child(cls.query_file)) as fobj:
            query = fobj.read()

        return impala_execute(query, kwargs)

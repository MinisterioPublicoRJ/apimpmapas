from dominio.db_connectors import execute as impala_execute
from dominio.exceptions import APIEmptyResultError


class GenericDAO:
    """Classe que implementa métodos genéricos de execução de query no
    impala a partir de um arquivo, e posterior serialização.

    Atributos:
    - QUERIES_DIR (path): Caminho da pasta onde estão as queries.
    - query_file (str): Nome do arquivo .sql contendo a query a executar.
    - columns (list): Lista de nome das colunas a usar na serialização.
    - serializer (Serializer): Serializador a ser utilizado (opcional).
    - table_namespaces (dict): Define os schemas a serem formatados na query.
    """

    QUERIES_DIR = ""
    query_file = ""
    columns = []
    serializer = None
    table_namespaces = {}

    @classmethod
    def query(cls):
        with open(cls.QUERIES_DIR.child(cls.query_file)) as fobj:
            query = fobj.read()

        return query.format(**cls.table_namespaces)

    @classmethod
    def execute(cls, **kwargs):
        return impala_execute(cls.query(), kwargs)

    @classmethod
    def serialize(cls, result_set):
        ser_data = [dict(zip(cls.columns, row)) for row in result_set]
        if cls.serializer:
            ser_data = cls.serializer(ser_data, many=True).data
        return ser_data

    @classmethod
    def get(cls, accept_empty=False, **kwargs):
        result_set = cls.execute(**kwargs)
        if not result_set and not accept_empty:
            cls.raise_empty_result_error()

        return cls.serialize(result_set)

    @classmethod
    def raise_empty_result_error(cls):
        raise APIEmptyResultError


class SingleDataObjectDAO(GenericDAO):
    @classmethod
    def serialize(cls, result_set):
        data = super().serialize(result_set)
        return data[0] if data else {}

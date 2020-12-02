from django.conf import settings

from dominio.dao import GenericDAO, SingleDataObjectDAO
from dominio.db_connectors import execute as impala_execute
from dominio.login import serializers
from lupa.db_connectors import oracle_access


class ListaOrgaosDAO(GenericDAO):
    QUERIES_DIR = settings.BASE_DIR.child("dominio", "login", "queries")
    query_file = "lista_orgaos.sql"
    columns = [
        "cdorgao",
        "nm_org",
        "matricula",
        "cpf",
        "nome",
        "sexo",
        "pess_dk",
    ]
    serializer = serializers.ListaOrgaosSerializer

    @classmethod
    def execute(cls, **kwargs):
        return oracle_access(cls.query(), kwargs)


class ListaTodosOrgaosDAO(GenericDAO):
    QUERIES_DIR = settings.BASE_DIR.child("dominio", "login", "queries")
    query_file = "lista_todos_orgaos.sql"
    columns = [
        "cdorgao",
        "nm_org",
        "matricula",
        "cpf",
        "nome",
        "sexo",
        "pess_dk",
    ]
    serializer = serializers.ListaOrgaosSerializer

    @classmethod
    def execute(cls, **kwargs):
        return oracle_access(cls.query(), kwargs)


class PIPValidasDAO(GenericDAO):
    QUERIES_DIR = settings.BASE_DIR.child("dominio", "login", "queries")
    query_file = "pip_validas.sql"
    columns = ["id_orgao"]
    serializer = serializers.PIPValidasSerializer
    table_namespaces = {"schema": settings.TABLE_NAMESPACE}


class DadosUsuarioDAO(SingleDataObjectDAO):
    QUERIES_DIR = settings.BASE_DIR.child("dominio", "login", "queries")
    query_file = "dados_usuario.sql"
    columns = ["matricula", "cpf", "nome", "sexo", "pess_dk"]
    serializer = serializers.DadosUsuarioSerializer
    many = False

    @classmethod
    def execute(cls, **kwargs):
        return oracle_access(cls.query(), kwargs)


class DPsPIPDAO(SingleDataObjectDAO):
    QUERIES_DIR = settings.BASE_DIR.child("dominio", "login", "queries")
    query_file = "get_dps_orgao.sql"
    columns = ["id_orgao", "dps"]
    serializer = serializers.DPsPIPSerializer
    table_namespaces = {"schema": settings.TABLE_NAMESPACE}


class ListaDPsPIPsDAO(GenericDAO):
    QUERIES_DIR = settings.BASE_DIR.child("dominio", "login", "queries")
    query_file = "get_lista_dps.sql"
    columns = ["id_orgao", "dps"]
    serializer = serializers.DPsPIPSerializer
    table_namespaces = {"schema": settings.TABLE_NAMESPACE}


class AtribuicoesOrgaosDAO(SingleDataObjectDAO):
    QUERIES_DIR = settings.BASE_DIR.child("dominio", "login", "queries")
    query_file = "get_atribuicoes_orgaos.sql"
    columns = ["atribuicao"]
    table_namespaces = {"schema": settings.TABLE_NAMESPACE}

    @classmethod
    def execute(cls, **kwargs):
        ids_orgaos = kwargs.get("ids_orgaos")
        prep_stat = {f"id_orgao_{i}": v for i, v in enumerate(ids_orgaos)}
        kwargs["ids_orgaos"] = prep_stat

        params = ",".join([f":id_orgao_{i}" for i in range(len(ids_orgaos))])
        query = cls.query().replace(":ids_orgaos", params)
        return impala_execute(query, prep_stat)

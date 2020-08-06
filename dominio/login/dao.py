from django.conf import settings

from dominio.dao import GenericDAO, SingleDataObjectDAO
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


class ListaOrgaosPessoalDAO(ListaOrgaosDAO):
    query_file = "lista_orgaos_pessoal.sql"
    serializer = serializers.ListaOrgaosSerializer


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

from django.conf import settings

from dominio.dao import GenericDAO, SingleDataObjectDAO
from dominio.login import serializers
from lupa.db_connectors import oracle_access


class ListaOrgaosDAO(GenericDAO):
    QUERIES_DIR = settings.BASE_DIR.child("dominio", "login", "queries")
    query_file = "lista_orgaos.sql"
    columns = ["cdorgao", "nm_org"]
    serializer = serializers.ListaOrgaosSerializer

    @classmethod
    def execute(cls, **kwargs):
        return oracle_access(cls.query(), kwargs)


class ListaOrgaosPessoalDAO(GenericDAO):
    QUERIES_DIR = settings.BASE_DIR.child("dominio", "login", "queries")
    query_file = "lista_orgaos_pessoal.sql"
    columns = ["cdorgao", "nm_org"]
    serializer = serializers.ListaOrgaosSerializer

    @classmethod
    def execute(cls, **kwargs):
        return oracle_access(cls.query(), kwargs)


class DadosUsuarioDAO(SingleDataObjectDAO):
    QUERIES_DIR = settings.BASE_DIR.child("dominio", "login", "queries")
    query_file = "dados_usuario.sql"
    columns = ["matricula", "cpf", "nome", "sexo", "pess_dk"]
    serializer = serializers.DadosUsuarioSerializer
    many = False

    @classmethod
    def execute(cls, **kwargs):
        return oracle_access(cls.query(), kwargs)

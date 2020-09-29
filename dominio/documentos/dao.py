from django.conf import settings

from dominio.dao import SingleDataObjectDAO


class MinutaPrescricaoDAO(SingleDataObjectDAO):
    QUERIES_DIR = settings.BASE_DIR.child("dominio", "documentos", "queries")
    query_file = "minuta_prescricao.sql"
    columns = [
        "num_procedimento",
        "data_fato",
        "orgao_responsavel",
        "comarca_tj",
        "tempo_passado",
        "assunto_docto",
        "lei_docto"
    ]
    table_namespaces = {
        "schema": settings.EXADATA_NAMESPACE,
    }


class DadosUsuarioDAO(SingleDataObjectDAO):
    QUERIES_DIR = settings.BASE_DIR.child("dominio", "documentos", "queries")
    query_file = "funcionario.sql"
    columns = [
        "matricula",
        "nome",
        "cargo"
    ]
    table_namespaces = {
        "schema": settings.EXADATA_NAMESPACE,
    }

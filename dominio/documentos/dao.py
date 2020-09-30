from django.conf import settings

from dominio.dao import SingleDataObjectDAO


class DocumentosDAO(SingleDataObjectDAO):
    QUERIES_DIR = settings.BASE_DIR.child("dominio", "documentos", "queries")
    table_namespaces = {
        "schema": settings.EXADATA_NAMESPACE,
    }

class MinutaPrescricaoDAO(DocumentosDAO):
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


class DadosUsuarioDAO(DocumentosDAO):
    query_file = "funcionario.sql"
    columns = [
        "matricula",
        "nome"
    ]


class DadosPromotorDAO(DocumentosDAO):
    query_file = "promotor.sql"
    columns = [
        "matricula",
        "nome"
    ]

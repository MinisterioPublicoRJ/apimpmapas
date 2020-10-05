from django.conf import settings

from dominio.dao import GenericDAO, SingleDataObjectDAO


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
    ]


class DadosPromotorDAO(DocumentosDAO):
    query_file = "dados_promotor.sql"
    columns = [
        "matricula_promotor",
        "nome_promotor",
    ]


class DadosAssuntoDAO(GenericDAO):
    QUERIES_DIR = settings.BASE_DIR.child("dominio", "documentos", "queries")
    query_file = "dados_assunto.sql"
    table_namespaces = {
        "schema": settings.EXADATA_NAMESPACE,
        "schema_aux": settings.TABLE_NAMESPACE
    }
    columns = [
        "nome_delito",
        "lei_delito",
        "max_pena",
        "multiplicador",
    ]

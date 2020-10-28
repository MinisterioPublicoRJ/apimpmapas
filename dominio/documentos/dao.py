from django.conf import settings

from dominio.dao import GenericDAO, SingleDataObjectDAO
from dominio.documentos.serializers import ComunicacaoCSMPSerializer


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
        "sexo",
    ]

    @classmethod
    def serialize(cls, result_set):
        ser_data = super().serialize(result_set)
        ser_data["matricula_promotor"] = str(
            int(ser_data["matricula_promotor"])
        )
        return ser_data


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


class ProrrogacaoICDAO(DocumentosDAO):
    query_file = "prorrogacao_ic.sql"
    columns = [
        "num_procedimento",
        "comarca",
    ]


class ProrrogacaoPPDAO(DocumentosDAO):
    query_file = "prorrogacao_pp.sql"
    columns = [
        "num_procedimento",
        "comarca",
    ]


class InstauracaoICDAO(DocumentosDAO):
    table_namespaces = {
        "schema": settings.EXADATA_NAMESPACE,
        "schema_aux": settings.TABLE_NAMESPACE,
    }
    query_file = "instauracao_ic.sql"
    columns = [
        "num_procedimento",
        "nome_promotoria",
        "comarca",
        "objeto",
        "codigo_assunto",
        "atribuicao",
        "ementa",
        "investigados",
    ]


class ListaROsAusentesDAO(GenericDAO):
    QUERIES_DIR = settings.BASE_DIR.child("dominio", "documentos", "queries")
    query_file = "lista_ros_ausentes.sql"
    columns = ["proc_numero_serial"]
    table_namespaces = {
        "schema_opengeo": settings.SCHEMA_OPENGEO_BDA
    }


class ComunicacaoCSMPDAO(GenericDAO):
    QUERIES_DIR = settings.BASE_DIR.child("dominio", "documentos", "queries")
    query_file = "procedimentos_comunicacao_csmp.sql"
    table_namespaces = {
        "schema": settings.EXADATA_NAMESPACE,
        "schema_aux": settings.TABLE_NAMESPACE,
    }
    columns = [
        "nome_promotoria",
        "num_procedimento",
        "data_cadastro",
        "comarca",
        "objeto",
        "ementa",
        "investigados"
    ]
    serializer = ComunicacaoCSMPSerializer

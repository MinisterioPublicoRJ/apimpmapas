from django.conf import settings

from dominio.dao import GenericDAO


class GenericTutelaDAO(GenericDAO):
    QUERIES_DIR = settings.BASE_DIR.child("dominio", "tutela", "queries")


class TempoTramitacaoIntegradoDAO(GenericTutelaDAO):
    query_file = "tempo_tramitacao_integrado.sql"
    columns = [
        "id_orgao",
        "tp_tempo",
        "media_orgao",
        "minimo_orgao",
        "maximo_orgao",
        "mediana_orgao",
        "media_pacote",
        "minimo_pacote",
        "maximo_pacote",
        "mediana_pacote"
    ]
    table_namespaces = {"schema": settings.TABLE_NAMESPACE}


class TempoTramitacaoDAO(GenericTutelaDAO):
    query_file = "tempo_tramitacao.sql"
    columns = [
        "id_orgao",
        "media_orgao",
        "minimo_orgao",
        "maximo_orgao",
        "mediana_orgao",
        "media_pacote",
        "minimo_pacote",
        "maximo_pacote",
        "mediana_pacote",
        "media_pacote_t1",
        "minimo_pacote_t1",
        "maximo_pacote_t1",
        "mediana_pacote_t1",
        "media_orgao_t1",
        "minimo_orgao_t1",
        "maximo_orgao_t1",
        "mediana_orgao_t1",
        "media_pacote_t2",
        "minimo_pacote_t2",
        "maximo_pacote_t2",
        "mediana_pacote_t2",
        "media_orgao_t2",
        "minimo_orgao_t2",
        "maximo_orgao_t2",
        "mediana_orgao_t2",
    ]
    table_namespaces = {"schema": settings.TABLE_NAMESPACE}


class ComparadorRadaresDAO(GenericTutelaDAO):
    query_file = "comparador_radares.sql"
    columns = [
        "orgao_id",
        "orgao_codamp",
        "orgi_nm_orgao",
        "perc_arquivamentos",
        "perc_indeferimentos",
        "perc_instauracoes",
        "perc_tac",
        "perc_acoes",
    ]
    table_namespaces = {"schema": settings.TABLE_NAMESPACE}

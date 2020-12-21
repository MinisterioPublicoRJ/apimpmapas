from django.conf import settings

from dominio.dao import GenericDAO, SingleDataObjectDAO
from dominio.tutela.serializers import (
    OutliersSerializer,
    SaidasSerializer,
    EntradasSerializer,
    ListaProcessosSerializer,
    RadarPerformanceSerializer
)
from dominio.utils import format_text


class GenericTutelaDAO(GenericDAO):
    QUERIES_DIR = settings.BASE_DIR.child("dominio", "tutela", "queries")


class OutliersDAO(GenericTutelaDAO, SingleDataObjectDAO):
    query_file = "outliers.sql"
    columns = [
        "cod_orgao",
        "acervo_qtd",
        "cod_atribuicao",
        "minimo",
        "maximo",
        "media",
        "primeiro_quartil",
        "mediana",
        "terceiro_quartil",
        "iqr",
        "lout",
        "hout",
        "dt_inclusao"
    ]
    table_namespaces = {"schema": settings.TABLE_NAMESPACE}
    serializer = OutliersSerializer


class SaidasDAO(GenericTutelaDAO, SingleDataObjectDAO):
    query_file = "saidas.sql"
    columns = [
        "saidas",
        "id_orgao",
        "cod_pct",
        "percent_rank",
        "dt_calculo"
    ]
    table_namespaces = {"schema": settings.TABLE_NAMESPACE}
    serializer = SaidasSerializer


class EntradasDAO(GenericTutelaDAO, SingleDataObjectDAO):
    query_file = "entradas.sql"
    columns = [
        "nr_entradas_hoje",
        "minimo",
        "maximo",
        "media",
        "primeiro_quartil",
        "mediana",
        "terceiro_quartil",
        "iqr",
        "lout",
        "hout"
    ]
    table_namespaces = {"schema": settings.TABLE_NAMESPACE}
    serializer = EntradasSerializer


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


class ListaProcessosDAO(GenericTutelaDAO):
    query_file = "lista_processos.sql"
    columns = [
        "id_orgao",
        "classe_documento",
        "docu_nr_mp",
        "docu_nr_externo",
        "docu_etiqueta",
        "docu_personagens",
        "representante_dk",
        "dt_ultimo_andamento",
        "ultimo_andamento",
        "url_tjrj"
    ]
    table_namespaces = {"schema": settings.TABLE_NAMESPACE}
    serializer = ListaProcessosSerializer


class ListaInvestigacoesDAO(GenericTutelaDAO):
    query_file = "lista_investigacoes.sql"
    columns = [
        "id_orgao",
        "classe_documento",
        "docu_nr_mp",
        "docu_nr_externo",
        "docu_etiqueta",
        "docu_personagens",
        "representante_dk",
        "dt_ultimo_andamento",
        "ultimo_andamento",
        "url_tjrj"
    ]
    table_namespaces = {"schema": settings.TABLE_NAMESPACE}
    # Mesmo formato de dados que a Lista de Processos
    serializer = ListaProcessosSerializer


class RadarPerformanceDAO(GenericTutelaDAO, SingleDataObjectDAO):
    query_file = "radar_performance.sql"
    columns = [
        "cod_pct",
        "pacote_atribuicao",
        "orgao_id",
        "nr_arquivamentos",
        "nr_indeferimentos",
        "nr_instauracoes",
        "nr_tac",
        "nr_acoes",
        "max_pacote_arquivamentos",
        "max_pacote_indeferimentos",
        "max_pacote_instauracoes",
        "max_pacote_tac",
        "max_pacote_acoes",
        "perc_arquivamentos",
        "perc_indeferimentos",
        "perc_instauracoes",
        "perc_tac",
        "perc_acoes",
        "med_pacote_aquivamentos",
        "med_pacote_indeferimentos",
        "med_pacote_instauracoes",
        "med_pacote_tac",
        "med_pacote_acoes",
        "var_med_arquivamentos",
        "var_med_indeferimentos",
        "var_med_instauracoes",
        "var_med_tac",
        "var_med_acoes",
        "dt_calculo",
        "nm_max_arquivamentos",
        "nm_max_indeferimentos",
        "nm_max_instauracoes",
        "nm_max_tac",
        "nm_max_acoes",
    ]
    table_namespaces = {"schema": settings.TABLE_NAMESPACE}
    serializer = RadarPerformanceSerializer

    @classmethod
    def serialize(cls, result_set):
        ser_data = super().serialize(result_set)

        format_fields = [
            "nm_max_arquivamentos", "nm_max_indeferimentos",
            "nm_max_instauracoes", "nm_max_tac", "nm_max_acoes"
        ]
        for field in format_fields:
            ser_data[field] = format_text(ser_data[field])

        return ser_data


class ComparadorRadaresDAO(GenericTutelaDAO):
    query_file = "comparador_radares.sql"
    columns = [
        "orgao_id",
        "orgao_codamp",
        "orgi_nm_orgao",
        "perc_arquivamentos",
        "perc_indeferimentos",
        "perc_tac",
        "perc_instauracoes",
        "perc_acoes",
    ]
    table_namespaces = {"schema": settings.TABLE_NAMESPACE}

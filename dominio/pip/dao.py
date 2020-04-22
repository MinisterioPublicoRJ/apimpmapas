from django.conf import settings

from dominio.db_connectors import execute as impala_execute
from dominio.utils import format_text


QUERIES_DIR = settings.BASE_DIR.child("dominio", "pip", "queries")


class PIPRadarPerformanceDAO:
    query_file = "pip_radar_performance.sql"
    columns = [
        "aisp_codigo",
        "aisp_nome",
        "orgao_id",
        "nr_denuncias",
        "nr_cautelares",
        "nr_acordos_n_persecucao",
        "nr_arquivamentos",
        "nr_aberturas_vista",
        "max_aisp_denuncias",
        "max_aisp_cautelares",
        "max_aisp_acordos",
        "max_aisp_arquivamentos",
        "max_aisp_aberturas_vista",
        "perc_denuncias",
        "perc_cautelares",
        "perc_acordos",
        "perc_arquivamentos",
        "perc_aberturas_vista",
        "med_aisp_denuncias",
        "med_aisp_cautelares",
        "med_aisp_acordos",
        "med_aisp_arquivamentos",
        "med_aisp_aberturas_vista",
        "var_med_denuncias",
        "var_med_cautelares",
        "var_med_acordos",
        "var_med_arquivamentos",
        "var_med_aberturas_vista",
        "dt_calculo",
        "nm_max_denuncias",
        "nm_max_cautelares",
        "nm_max_acordos",
        "nm_max_arquivamentos",
        "nm_max_abeturas_vista",
    ]

    @classmethod
    def execute(cls, **kwargs):
        with open(QUERIES_DIR.child(cls.query_file)) as fobj:
            query = fobj.read()

        return impala_execute(query, kwargs)

    @classmethod
    def serialize(cls, result_set):
        ser_data = dict(zip(cls.columns, result_set[0]))
        for column, value in ser_data.items():
            if column.startswith("nm_max"):
                ser_data[column] = format_text(value)

        return ser_data

    @classmethod
    def get(cls, **kwargs):
        result_set = cls.execute(**kwargs)
        return cls.serialize(result_set)

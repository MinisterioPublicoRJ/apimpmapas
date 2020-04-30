from functools import lru_cache

from django.conf import settings

from dominio.db_connectors import execute as impala_execute, get_hbase_table
from dominio.exceptions import APIEmptyResultError
from dominio.utils import format_text, hbase_encode_row, hbase_decode_row
from dominio.pip.serializers import PIPPrincipaisInvestigadosSerializer


QUERIES_DIR = settings.BASE_DIR.child("dominio", "pip", "queries")


class GenericDAO:
    query_file = ""
    columns = []
    serializer = None
    table_namespaces = {}

    @classmethod
    def query(cls):
        with open(QUERIES_DIR.child(cls.query_file)) as fobj:
            query = fobj.read()

        return query.format(**cls.table_namespaces)

    @classmethod
    def execute(cls, **kwargs):
        return impala_execute(cls.query(), kwargs)

    @classmethod
    def serialize(cls, result_set):
        ser_data = [dict(zip(cls.columns, row)) for row in result_set]
        if cls.serializer:
            ser_data = cls.serializer(ser_data, many=True).data
        return ser_data

    @classmethod
    def get(cls, **kwargs):
        result_set = cls.execute(**kwargs)
        if not result_set:
            raise APIEmptyResultError

        return cls.serialize(result_set)


class PIPRadarPerformanceDAO(GenericDAO):
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
    table_namespaces = {"schema": settings.TABLE_NAMESPACE}

    @classmethod
    @lru_cache(maxsize=None)
    def query(cls):
        return super().query()

    @classmethod
    def serialize(cls, result_set):
        ser_data = super().serialize(result_set)[0]
        for column, value in ser_data.items():
            if column.startswith("nm_max"):
                ser_data[column] = format_text(value)

        return ser_data


class PIPPrincipaisInvestigadosDAO(GenericDAO):
    hbase_table_name = "pip_investigados_flags"
    query_file = "pip_principais_investigados.sql"
    columns = [
        "nm_investigado",
        "pip_codigo",
        "nr_investigacoes",
    ]
    table_namespaces = {"schema": settings.TABLE_NAMESPACE}
    serializer = PIPPrincipaisInvestigadosSerializer

    @classmethod
    @lru_cache(maxsize=None)
    def query(cls):
        return super().query()

    @classmethod
    def get_hbase_flags(cls, orgao_id, cpf):
        # orgao_id e cpf precisam ser str
        row_prefix = bytes(orgao_id + cpf, encoding='utf-8')
        hbase = get_hbase_table(cls.hbase_table_name)

        data = {
            drow[1]['identificacao:nm_personagem']:
                {
                    'is_pinned': (
                        drow[1]['flags:is_pinned']
                        if 'flags:is_pinned' in drow[1]
                        else False
                    ),
                    'is_removed': (
                        drow[1]['flags:is_removed']
                        if 'flags:is_removed' in drow[1]
                        else False
                    )
                }
            for drow in [
                hbase_decode_row(row)
                for row in hbase.scan(row_prefix=row_prefix)
            ]
        }

        return data

    @classmethod
    def save_hbase_flags(cls, orgao_id, cpf, nm_personagem,
                         is_pinned, is_removed):
        row_key = orgao_id + cpf + nm_personagem
        data = {
            'identificacao:orgao_id': orgao_id,
            'identificacao:cpf': cpf,
            'identificacao:nm_personagem': nm_personagem
        }
        if is_pinned:
            data['flags:is_pinned'] = is_pinned
        if is_removed:
            data['flags:is_removed'] = is_removed
        row = (row_key, data)

        hbase = get_hbase_table(cls.hbase_table_name)
        hbase.put(*hbase_encode_row(row))

        return data

    @classmethod
    def get(cls, orgao_id, cpf):
        hbase_flags = cls.get_hbase_flags(orgao_id, cpf)
        data = super().get(orgao_id=int(orgao_id))

        for row in data:
            investigado = row['nm_investigado']
            row['is_pinned'] = (
                hbase_flags[investigado]['is_pinned']
                if investigado in hbase_flags
                and 'is_pinned' in hbase_flags[investigado]
                else False
            )
            row['is_removed'] = (
                hbase_flags[investigado]['is_removed']
                if investigado in hbase_flags
                and 'is_removed' in hbase_flags[investigado]
                else False
            )

        data = [row for row in data if not row['is_removed']]

        data = sorted(
            data,
            key=lambda k:
                (-k['is_pinned'], -k['nr_investigacoes'], k['nm_investigado'])
        )

        return data

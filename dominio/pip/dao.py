from functools import lru_cache

from django.conf import settings
from django.core.cache import cache

from dominio.db_connectors import get_hbase_table
from dominio.utils import (
    format_text,
    hbase_encode_row,
    hbase_decode_row,
)
from dominio.pip.serializers import (
    PIPPrincipaisInvestigadosSerializer,
    PIPIndicadoresSucessoParser,
    PIPPrincipaisInvestigadosListaSerializer,
    PIPPrincipaisInvestigadosPerfilSerializer,
)

from dominio.utils import is_valid_cpf, is_valid_rg
from dominio.dao import GenericDAO


class GenericPIPDAO(GenericDAO):
    QUERIES_DIR = settings.BASE_DIR.child("dominio", "pip", "queries")


class PIPRadarPerformanceDAO(GenericPIPDAO):
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
        "cod_pct"
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


class PIPPrincipaisInvestigadosDAO(GenericPIPDAO):
    hbase_table_name = "pip_investigados_flags"
    hbase_namespace = settings.PROMOTRON_HBASE_NAMESPACE
    query_file = "pip_principais_investigados.sql"
    columns = [
        "nm_investigado",
        "representante_dk",
        "pip_codigo",
        "nr_investigacoes",
        "flag_multipromotoria",
        "flag_top50"
    ]
    table_namespaces = {"schema": settings.TABLE_NAMESPACE}
    serializer = PIPPrincipaisInvestigadosSerializer
    cache_prefix = 'PIP_PRINCIPAIS_INVESTIGADOS'

    @classmethod
    @lru_cache(maxsize=None)
    def query(cls):
        return super().query()

    @classmethod
    def get_hbase_flags(cls, orgao_id, cpf):
        # orgao_id e cpf precisam ser str
        row_prefix = bytes(orgao_id + cpf, encoding="utf-8")
        hbase = get_hbase_table(cls.hbase_namespace + cls.hbase_table_name)

        data = {
            drow[1]["identificacao:representante_dk"]:
                {
                    "is_pinned": (
                        drow[1]["flags:is_pinned"]
                        if "flags:is_pinned" in drow[1]
                        else False
                    ),
                    "is_removed": (
                        drow[1]["flags:is_removed"]
                        if "flags:is_removed" in drow[1]
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
    def save_hbase_flags(cls, orgao_id, cpf, representante_dk, action):
        row_key = orgao_id + cpf + representante_dk
        hbase = get_hbase_table(cls.hbase_namespace + cls.hbase_table_name)

        data = {
            "identificacao:orgao_id": orgao_id,
            "identificacao:cpf": cpf,
            "identificacao:representante_dk": representante_dk
        }
        row = (row_key, data)

        if action == "unpin":
            hbase.delete(bytes(row_key, "utf-8"), columns=["flags:is_pinned"])
        elif action == "unremove":
            hbase.delete(bytes(row_key, "utf-8"), columns=["flags:is_removed"])
        elif action == "pin":
            data["flags:is_pinned"] = True
            hbase.put(*hbase_encode_row(row))
        elif action == "remove":
            data["flags:is_removed"] = True
            hbase.put(*hbase_encode_row(row))

        # Flags precisam estar atualizadas no próximo GET
        cache_key = '{}_FLAGS_{}_{}'.format(cls.cache_prefix, orgao_id, cpf)
        cache.delete(cache_key)

        return {"status": "Success!"}

    @classmethod
    def get(cls, orgao_id, cpf):
        cache_key = '{}_FLAGS_{}_{}'.format(cls.cache_prefix, orgao_id, cpf)
        hbase_flags = cache.get(cache_key, default=None)
        if not hbase_flags:
            hbase_flags = cls.get_hbase_flags(orgao_id, cpf)
            cache.set(cache_key, hbase_flags, timeout=settings.CACHE_TIMEOUT)

        cache_key = '{}_DATA_{}'.format(cls.cache_prefix, orgao_id)
        data = cache.get(cache_key, default=None)
        if not data:
            digit = int(orgao_id[-1])
            data = super().get(orgao_id=int(orgao_id), digit=digit)
            cache.set(cache_key, data, timeout=settings.CACHE_TIMEOUT)

        # Flags e dados precisam estar juntos para o front
        for row in data:
            investigado_dk = row["representante_dk"]
            if investigado_dk in hbase_flags:
                row["is_pinned"] = (
                    hbase_flags[investigado_dk]["is_pinned"]
                    if "is_pinned" in hbase_flags[investigado_dk]
                    else False
                )
                row["is_removed"] = (
                    hbase_flags[investigado_dk]["is_removed"]
                    if "is_removed" in hbase_flags[investigado_dk]
                    else False
                )
            else:
                row["is_pinned"] = False
                row["is_removed"] = False

        # Nomes que foram removidos não precisam ser entregues
        data = [row for row in data if not row["is_removed"]]

        data = sorted(
            data,
            key=lambda k:
                (-k["is_pinned"], -k["nr_investigacoes"], k["nm_investigado"])
        )

        return data


class PIPPrincipaisInvestigadosPerfilDAO(GenericPIPDAO):
    query_file = "pip_principais_investigados_perfil.sql"
    columns = [
        "pess_dk",
        "nm_investigado",
        "nm_mae",
        "cpf",
        "rg",
        "dt_nasc",
        "nm_pesj",
        "cnpj"
    ]
    table_namespaces = {
        "schema_exadata": settings.EXADATA_NAMESPACE,
        "schema": settings.TABLE_NAMESPACE
    }
    serializer = PIPPrincipaisInvestigadosPerfilSerializer
    cache_prefix = 'PIP_PRINCIPAIS_INVESTIGADOS_PERFIL'

    @classmethod
    def get(cls, accept_empty=False, **kwargs):
        cache_key = '{}_DATA_{}'.format(
            cls.cache_prefix, kwargs.get("dk")
        )
        data = cache.get(cache_key, default=None)
        if not data:
            data = super().get(accept_empty, **kwargs)
            cache.set(cache_key, data, timeout=settings.CACHE_TIMEOUT)
        return data

    @classmethod
    def serialize(cls, result_set):
        ser_data = super().serialize(result_set)

        # Verifica se é pessoa física ou jurídica
        keys_pesj = cls.columns[0:1] + cls.columns[6:]
        keys_pesf = cls.columns[0:6]
        keys_to_keep = (
            keys_pesj if ser_data and ser_data[0]['nm_pesj']
            else keys_pesf
        )

        ser_data = [
            {key: row[key] for key in row if key in keys_to_keep}
            for row in ser_data
        ]

        return ser_data

    @classmethod
    def get_header_info(cls, data):
        if not data:
            return {}

        header = data[0].copy()
        header['pess_dk'] = None
        if 'cpf' in header:
            header['cpf'] = (
                header['cpf'] if is_valid_cpf(header['cpf'])
                else None
            )
            header['rg'] = header['rg'] if is_valid_rg(header['rg']) else None
            for profile in data:
                if not header['nm_mae']:
                    header['nm_mae'] = profile['nm_mae']
                if not header['dt_nasc']:
                    header['dt_nasc'] = profile['dt_nasc']
                if not header['cpf'] and is_valid_cpf(profile['cpf']):
                    header['cpf'] = profile['cpf']
                if not header['rg'] and is_valid_rg(profile['rg']):
                    header['rg'] = profile['rg']
        else:
            for profile in data:
                if not header['cnpj']:
                    header['cnpj'] = profile['cnpj']
                if not header['nm_pesj']:
                    header['nm_pesj'] = profile['nm_pesj']
        return header


class PIPPrincipaisInvestigadosListaDAO(GenericPIPDAO):
    query_file = "pip_principais_investigados_lista.sql"
    columns = [
        "pess_dk",
        "coautores",
        "documento_nr_mp",
        "nm_orgao",
        "assuntos",
        "fase_documento",
        "dt_ultimo_andamento",
        "desc_ultimo_andamento",
    ]
    table_namespaces = {"schema": settings.TABLE_NAMESPACE}
    serializer = PIPPrincipaisInvestigadosListaSerializer
    cache_prefix = 'PIP_PRINCIPAIS_INVESTIGADOS_LISTA'

    @classmethod
    def serialize(cls, result_set):
        # Assuntos vem separados por ' --- ' no banco
        idx = cls.columns.index('assuntos')
        result_set = [
            row[:idx] + tuple([row[idx].split(' --- ')]) + row[idx+1:]
            if isinstance(row[idx], str)
            else row
            for row in result_set
        ]

        ser_data = super().serialize(result_set)
        for row in ser_data:
            nm_orgao = row['nm_orgao']
            row['nm_orgao'] = format_text(nm_orgao)

        return ser_data

    @classmethod
    def get(cls, accept_empty=False, **kwargs):
        cache_key = '{}_DATA_{}'.format(
            cls.cache_prefix, kwargs.get("dk")
        )
        data = cache.get(cache_key, default=None)
        if not data:
            data = super().get(accept_empty, **kwargs)
            cache.set(cache_key, data, timeout=settings.CACHE_TIMEOUT)

        pess_dk = kwargs.get("pess_dk")
        if pess_dk:
            data = [x for x in data if x['pess_dk'] == pess_dk]
        return data


class PIPIndicadoresDeSucessoDAO(GenericPIPDAO):
    query_file = "pip_indicadores_sucesso.sql"
    table_namespaces = {"schema": settings.TABLE_NAMESPACE}
    serializer = PIPIndicadoresSucessoParser
    columns = ["orgao_id", "indice", "tipo"]


class PIPComparadorRadaresDAO(GenericPIPDAO):
    query_file = "pip_comparador_radares.sql"
    columns = [
        "orgao_id",
        "orgao_codamp",
        "orgi_nm_orgao",
        "perc_denuncias",
        "perc_cautelares",
        "perc_acordos",
        "perc_arquivamentos",
        "perc_aberturas_vista",
    ]
    table_namespaces = {"schema": settings.TABLE_NAMESPACE}

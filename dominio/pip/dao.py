from functools import lru_cache

from django.conf import settings
from django.core.cache import cache

from dominio.db_connectors import get_hbase_table
from dominio.exceptions import APIEmptyResultError
from dominio.utils import (
    format_text,
    hbase_encode_row,
    hbase_decode_row,
    get_top_n_orderby_value_as_dict,
    get_value_given_key,
)
from dominio.pip.serializers import (
    PIPPrincipaisInvestigadosSerializer,
    PIPIndicadoresSucessoParser,
    PIPDetalheAproveitamentosSerializer,
    PIPPrincipaisInvestigadosListaSerializer,
    PIPPrincipaisInvestigadosPerfilSerializer,
)

from .utils import get_top_n_by_aisp, get_orgaos_same_aisps
from dominio.dao import GenericDAO, SingleDataObjectDAO


class GenericPIPDAO(GenericDAO):
    QUERIES_DIR = settings.BASE_DIR.child("dominio", "pip", "queries")


class PIPDetalheAproveitamentosDAO(GenericPIPDAO):
    query_file = "pip_detalhe_aproveitamentos.sql"
    serializer = PIPDetalheAproveitamentosSerializer
    table_namespaces = {"schema": settings.TABLE_NAMESPACE}

    @classmethod
    @lru_cache(maxsize=None)
    def query(cls):
        return super().query()

    @classmethod
    def get(cls, **kwargs):
        data = super().execute(**kwargs)
        if not data:
            raise APIEmptyResultError

        orgao_id = kwargs['orgao_id']

        aisps, orgaos_same_aisps = get_orgaos_same_aisps(orgao_id)
        top_n_aisp = get_top_n_by_aisp(
            orgaos_same_aisps,
            data,
            name_position=1,
            value_position=2,
            name_fieldname="nm_promotoria",
            value_fieldname="nr_aproveitamentos_periodo",
            n=3,
        )
        for row in top_n_aisp:
            row['nm_promotoria'] = format_text(row['nm_promotoria'])

        nr_aproveitamentos_periodo = get_value_given_key(
            data, orgao_id, key_position=0, value_position=2
        )
        variacao_periodo = get_value_given_key(
            data, orgao_id, key_position=0, value_position=4
        )
        tamanho_periodo_dias = get_value_given_key(
            data, orgao_id, key_position=0, value_position=5
        )
        top_n_pacote = get_top_n_orderby_value_as_dict(
            data,
            name_position=1,
            value_position=2,
            name_fieldname="nm_promotoria",
            value_fieldname="nr_aproveitamentos_periodo",
            n=3,
        )
        for row in top_n_pacote:
            row['nm_promotoria'] = format_text(row['nm_promotoria'])

        data_obj = {
            "nr_aproveitamentos_periodo": nr_aproveitamentos_periodo,
            "variacao_periodo": variacao_periodo,
            "top_n_pacote": top_n_pacote,
            "nr_aisps": aisps,
            "top_n_aisp": top_n_aisp,
            "tamanho_periodo_dias": tamanho_periodo_dias,
        }
        data = cls.serializer(data_obj).data
        return data


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
            data = super().get(orgao_id=int(orgao_id))
            cache.set(cache_key, data, timeout=settings.CACHE_TIMEOUT)

        # Flags e dados precisam estar juntos para o front
        for row in data:
            investigado_dk = row["representante_dk"]
            row["is_pinned"] = (
                hbase_flags[investigado_dk]["is_pinned"]
                if investigado_dk in hbase_flags
                and "is_pinned" in hbase_flags[investigado_dk]
                else False
            )
            row["is_removed"] = (
                hbase_flags[investigado_dk]["is_removed"]
                if investigado_dk in hbase_flags
                and "is_removed" in hbase_flags[investigado_dk]
                else False
            )

        # Nomes que foram removidos não precisam ser entregues
        data = [row for row in data if not row["is_removed"]]

        data = sorted(
            data,
            key=lambda k:
                (-k["is_pinned"], -k["nr_investigacoes"], k["nm_investigado"])
        )

        return data


class PIPPrincipaisInvestigadosPerfilDAO(SingleDataObjectDAO, GenericPIPDAO):
    query_file = "pip_principais_investigados_perfil.sql"
    columns = [
        "nm_investigado",
        "nm_mae",
        "cpf",
        "rg",
        "dt_nasc",
    ]
    table_namespaces = {"schema": settings.EXADATA_NAMESPACE}
    serializer = PIPPrincipaisInvestigadosPerfilSerializer


class PIPPrincipaisInvestigadosListaDAO(GenericPIPDAO):
    query_file = "pip_principais_investigados_lista.sql"
    columns = [
        "representante_dk",
        "coautores",
        "tipo_personagem",
        "orgao_id",
        "documento_nr_mp",
        "documento_dt_cadastro",
        "documento_classe",
        "nm_orgao",
        "etiqueta",
        "assuntos",
        "fase_documento",
        "dt_ultimo_andamento",
        "desc_ultimo_andamento"
    ]
    table_namespaces = {"schema": settings.TABLE_NAMESPACE}
    serializer = PIPPrincipaisInvestigadosListaSerializer

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


class PIPIndicadoresDeSucessoDAO(GenericPIPDAO):
    query_file = "pip_indicadores_sucesso.sql"
    table_namespaces = {"schema": settings.TABLE_NAMESPACE}
    serializer = PIPIndicadoresSucessoParser
    columns = ["orgao_id", "indice", "tipo"]

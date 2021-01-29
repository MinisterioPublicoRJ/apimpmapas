from datetime import date

from django.http import FileResponse
from django.conf import settings

from dominio.dao import GenericDAO, SingleDataObjectDAO
from dominio.db_connectors import run_query
from dominio.alertas import serializers
from dominio.alertas.helper import ordem as alrt_ordem, headers as alrt_header
from dominio.alertas.exceptions import (
    APIInvalidOverlayType,
    APIMissingOverlayType,
    APIAlertTypeListNotConfigured,
)
from dominio.documentos.helpers import gera_planilha_excel


class AlertasDAO(GenericDAO):
    QUERIES_DIR = settings.BASE_DIR.child("dominio", "alertas", "queries")

    @classmethod
    def ordena_alertas(cls, alertas):
        ordem_dict = {s: i for i, s in enumerate(alrt_ordem)}
        alertas = [x for x in alertas if x["sigla"] in ordem_dict]
        return sorted(alertas, key=lambda x: ordem_dict[x["sigla"]])


class ResumoAlertasDAO(AlertasDAO):
    """
    Classe principal do Resumo dos Alertas.
    Esta classe executa todos os outros DAOs de resumo de alertas
    que herdam dela.
    """

    query_file = "resumo_alertas.sql"
    columns = ["sigla", "count"]
    table_namespaces = {
        "schema": settings.ALERTAS_NAMESPACE,
    }
    serializer = serializers.AlertasResumoSerializer

    @classmethod
    def get_all(cls, id_orgao):
        resumo = super().get(
            orgao_id=id_orgao,
            accept_empty=True
        )

        return cls.ordena_alertas(resumo)


class AlertaMGPDAO(AlertasDAO):
    table_namespaces = {"schema": settings.ALERTAS_NAMESPACE}
    query_file = "alertas_get.sql"
    columns = [
        "doc_dk",
        "num_doc",
        "data_alerta",
        "orgao",
        "dias_passados",
        "id_alerta",
        "sigla",
        "descricao",
        "classe_hierarquia",
        "num_externo",
        "alrt_key",
        # "flag_dispensado"
    ]
    serializer = serializers.AlertasListaSerializer

    @classmethod
    def execute(cls, **kwargs):
        return run_query(cls.query(), kwargs) or []

    @classmethod
    def get(cls, accept_empty=True, **kwargs):
        result_set = super().get(accept_empty=accept_empty, **kwargs)
        # result_set = [x for x in result_set if x['flag_dispensado'] == 0]
        return cls.ordena_alertas(result_set)


class AlertaComprasDAO(AlertasDAO):
    query_file = "alerta_compras.sql"
    columns = [
        "sigla",
        "contrato",
        "iditem",
        "contrato_iditem",
        "item",
        "alrt_key",
        # "flag_dispensado"
    ]
    serializer = serializers.AlertasComprasSerializer
    table_namespaces = {
        "schema": settings.ALERTAS_NAMESPACE,
    }

    @classmethod
    def get(cls, accept_empty=True, **kwargs):
        result_set = super().get(accept_empty=accept_empty, **kwargs)
        # TODO: Pode ser necessario entregar tudo no futuro, até dispensados
        # result_set = [x for x in result_set if x['flag_dispensado'] == 0]
        return result_set


# ------ DAOs relativos ao Overlay do Alerta

class AlertaOverlayPrescricaoDAO(AlertasDAO):
    query_file = "alerta_overlay_prescricao.sql"
    columns = [
        'tipo_penal',
        'nm_investigado',
        'max_pena',
        'delitos_multiplicadores',
        'fator_pena',
        'max_pena_fatorado',
        'dt_inicio_prescricao',
        'dt_fim_prescricao',
        'adpr_chave'
    ]
    serializer = serializers.AlertaOverlayPrescricaoSerializer
    table_namespaces = {
        "schema_exadata": settings.EXADATA_NAMESPACE,
        "schema": settings.ALERTAS_NAMESPACE
    }


class AlertaOverlayIC1ADAO(AlertasDAO, SingleDataObjectDAO):
    query_file = "alerta_overlay_ic1a.sql"
    columns = [
        'dt_fim_prazo',
        'dt_movimento',
        'desc_movimento'
    ]
    table_namespaces = {
        "schema": settings.ALERTAS_NAMESPACE,
        "schema_exadata": settings.EXADATA_NAMESPACE,
        "schema_exadata_aux": settings.TABLE_NAMESPACE
    }


class AlertaOverlayPA1ADAO(AlertasDAO, SingleDataObjectDAO):
    query_file = "alerta_overlay_pa1a.sql"
    columns = [
        'dt_fim_prazo',
        'docu_dt_cadastro'
    ]
    table_namespaces = {
        "schema_exadata": settings.EXADATA_NAMESPACE,
        "schema": settings.ALERTAS_NAMESPACE
    }


class AlertaOverlayPPFPDAO(AlertasDAO, SingleDataObjectDAO):
    query_file = "alerta_overlay_ppfp.sql"
    columns = [
        'docu_dt_cadastro'
    ]
    table_namespaces = {
        "schema_exadata": settings.EXADATA_NAMESPACE
    }


class AlertasOverlayDAO:
    _type_switcher = {
        'prescricao': AlertaOverlayPrescricaoDAO,
        'pa1a': AlertaOverlayPA1ADAO,
        'ic1a': AlertaOverlayIC1ADAO,
        'ppfp': AlertaOverlayPPFPDAO
    }

    @classmethod
    def get(cls, docu_dk, request):
        tipo = request.GET.get("tipo")
        if not tipo:
            raise APIMissingOverlayType

        DAO = cls.switcher(tipo)

        return DAO.get(
            docu_dk=docu_dk
        )

    @classmethod
    def switcher(cls, tipo):
        if tipo not in cls._type_switcher:
            raise APIInvalidOverlayType
        return cls._type_switcher[tipo]


class DetalheAlertaCompraDAO(SingleDataObjectDAO):
    QUERIES_DIR = settings.BASE_DIR.child("dominio", "alertas", "queries")
    serializer = serializers.DetalheAlertaSerializer

    query_file = "detalhe_alerta_compra.sql"
    columns = [
        "contratacao",
        "data_contratacao",
        "item_contratado",
        "var_perc",
    ]
    table_namespaces = {
        "schema_alertas": settings.ALERTAS_NAMESPACE,
    }


class DetalheAlertaISPSDAO(SingleDataObjectDAO):
    QUERIES_DIR = settings.BASE_DIR.child("dominio", "alertas", "queries")

    query_file = "detalhe_alerta_isps.sql"
    columns = [
        "municipio",
        "descricao",
    ]
    table_namespaces = {
        "schema": settings.ALERTAS_NAMESPACE,
    }


class BaixarAlertasDAO(AlertasDAO):
    table_namespaces = {
        "schema": settings.ALERTAS_NAMESPACE,
        "schema_exadata": settings.EXADATA_NAMESPACE,
    }

    _file_switcher = {
        'PRCR': 'baixar_alertas_mgp.sql',
        'PRCR1': 'baixar_alertas_mgp.sql',
        'PRCR2': 'baixar_alertas_mgp.sql',
        'PRCR3': 'baixar_alertas_mgp.sql',
        'PRCR4': 'baixar_alertas_mgp.sql',
        'COMP': 'baixar_alertas_comp.sql',
        'ISPS': 'baixar_alertas_isps.sql',
        'GATE': 'baixar_alertas_gate.sql',
        'MVVD': 'baixar_alertas_mgp.sql',
        'BDPA': 'baixar_alertas_mgp.sql',
        'IC1A': 'baixar_alertas_mgp.sql',
        'PA1A': 'baixar_alertas_mgp.sql',
        'PPFP': 'baixar_alertas_ppfp.sql',
        'PPPV': 'baixar_alertas_ppfp.sql',
        'OUVI': 'baixar_alertas_mgp.sql',
        'NF30': 'baixar_alertas_mgp.sql',
        'VADF': 'baixar_alertas_mgp.sql',
        'DT2I': 'baixar_alertas_mgp.sql',
        'DORD': 'baixar_alertas_mgp.sql',
        'DNTJ': 'baixar_alertas_mgp.sql',
    }

    @classmethod
    def get(cls, alrt_type, **kwargs):
        try:
            header = alrt_header[alrt_type]
            cls.query_file = cls._file_switcher[alrt_type]
        except KeyError:
            raise APIAlertTypeListNotConfigured

        kwargs['alrt_type'] = alrt_type
        data = cls.execute(**kwargs)
        if not data:
            cls.raise_empty_result_error()

        data = [x[:len(header)] for x in data]

        return FileResponse(
            gera_planilha_excel(
                data,
                header=header,
                sheet_title=f"Alertas {alrt_type}"
            ),
            filename=f"Alerta-{alrt_type}-{date.today()}.xlsx",
            as_attachment=True
        )

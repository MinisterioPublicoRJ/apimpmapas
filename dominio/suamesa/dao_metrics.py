from django.conf import settings

from dominio.suamesa.serializers import (
    MetricsDetalheDocumentoOrgaoCPFSerializer,
    MetricsDetalheDocumentoOrgaoSerializer,
)
from dominio.dao import SingleDataObjectDAO
from dominio.suamesa.exceptions import APIMissingRequestParameterSuaMesa


class MetricsDataObjectDAO(SingleDataObjectDAO):
    QUERIES_DIR = settings.BASE_DIR.child("dominio", "suamesa", "queries")
    table_namespaces = {"schema": settings.TABLE_NAMESPACE}
    required_parameters = []

    @classmethod
    def check_required_parameters(cls, **kwargs):
        for parameter in cls.required_parameters:
            if parameter not in kwargs:
                e = "Parâmetro '{}' não foi dado!".format(parameter)
                raise APIMissingRequestParameterSuaMesa(e)

    @classmethod
    def get(cls, accept_empty=True, **kwargs):
        cls.check_required_parameters(**kwargs)
        data = super().get(accept_empty=accept_empty, **kwargs)

        return {'metrics': data}


class MetricsDetalheDocumentoOrgaoDAO(MetricsDataObjectDAO):
    query_file = "detalhe_documento_orgao.sql"
    columns = [
        'tipo_detalhe',
        'intervalo',
        'nm_orgao',
        'cod_pacote',
        'orgao_id',
        'nr_documentos_distintos_atual',
        'nr_aberturas_vista_atual',
        'nr_aproveitamentos_atual',
        'nr_instaurados_atual',
        'acervo_anterior',
        'acervo_atual',
        'variacao_acervo',
        'nr_documentos_distintos_anterior',
        'nr_aberturas_vista_anterior',
        'nr_aproveitamentos_anterior',
        'nr_instaurados_anterior',
        'variacao_documentos_distintos',
        'variacao_aberturas_vista',
        'variacao_aproveitamentos',
        'variacao_instaurados'
    ]
    serializer = MetricsDetalheDocumentoOrgaoSerializer


class MetricsDetalheDocumentoOrgaoCPFDAO(MetricsDataObjectDAO):
    query_file = "detalhe_documento_orgao_cpf.sql"
    columns = [
        'tipo_detalhe',
        'intervalo',
        'orgao_id',
        'cpf',
        'nr_documentos_distintos_atual',
        'nr_aberturas_vista_atual',
        'nr_aproveitamentos_atual',
        'nr_instaurados_atual',
        'nr_documentos_distintos_anterior',
        'nr_aberturas_vista_anterior',
        'nr_aproveitamentos_anterior',
        'nr_instaurados_anterior',
        'variacao_documentos_distintos',
        'variacao_aberturas_vista',
        'variacao_aproveitamentos',
        'variacao_instaurados'
    ]
    serializer = MetricsDetalheDocumentoOrgaoCPFSerializer
    required_parameters = ['cpf']

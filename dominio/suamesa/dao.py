"""
Definição do DAO (Data Access Object) usado pela View do SuaMesa.

Este DAO irá pegar o tipo de dado a ser buscado (especificado no request),
e irá chamar a função apropriada para fazer esta busca.

Caso o tipo de dado não seja especificado, ou seja informado um tipo de dado
não definido, o DAO irá levantar uma exceção.
"""

from django.conf import settings

from dominio.suamesa.exceptions import (
    APIInvalidSuaMesaType,
    APIMissingSuaMesaType,
)
from dominio.suamesa import dao_functions
from dominio.suamesa.serializers import SuaMesaDetalheCPFSerializer
from dominio.dao import GenericDAO


class SuaMesaDAO:
    _type_switcher = {
        'vistas': dao_functions.get_vistas,
        'tutela_investigacoes': dao_functions.get_tutela_investigacoes,
        'tutela_processos': dao_functions.get_tutela_processos,
        'pip_inqueritos': dao_functions.get_pip_inqueritos,
        'pip_pics': dao_functions.get_pip_pics,
        'pip_aisp': dao_functions.get_pip_aisp,
        'tutela_finalizados': dao_functions.get_tutela_finalizados,
        'pip_finalizados': dao_functions.get_pip_finalizados
    }

    @classmethod
    def get(cls, orgao_id, request):
        tipo = request.GET.get("tipo")

        if not tipo:
            raise APIMissingSuaMesaType

        get_data = cls.switcher(tipo)
        return {'nr_documentos': get_data(orgao_id, request)}

    @classmethod
    def switcher(cls, tipo):
        if tipo not in cls._type_switcher:
            raise APIInvalidSuaMesaType
        return cls._type_switcher[tipo]


class SuaMesaDetalheCPFDAO(GenericDAO):
    QUERIES_DIR = settings.BASE_DIR.child("dominio", "suamesa", "queries")
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
        'variacao_nr_documentos_distintos',
        'variacao_nr_aberturas_vista',
        'variacao_nr_aproveitamentos',
        'variacao_nr_instaurados'
    ]
    serializer = SuaMesaDetalheCPFSerializer
    table_namespaces = {"schema": settings.TABLE_NAMESPACE}

    @classmethod
    def get(cls, orgao_id, request):
        kwargs = {
            'orgao_id': orgao_id,
            'tipo_detalhe': request.GET.get('tipo'),
            'cpf': request.GET.get('cpf'),
        }

        return super().get(**kwargs)


class SuaMesaDetalhePIPInqueritoDAO(SuaMesaDetalheCPFDAO):
    nome_tipo_tabela = 'pip_inqueritos'


class SuaMesaDetalhePIPPICSDAO(SuaMesaDetalheCPFDAO):
    nome_tipo_tabela = 'pip_pics'


class SuaMesaDetalheFactoryDAO(SuaMesaDAO):
    _type_switcher = {
        'pip_inqueritos': SuaMesaDetalhePIPInqueritoDAO,
        'pip_pics': SuaMesaDetalhePIPPICSDAO,
    }

    @classmethod
    def get(cls, orgao_id, request):
        tipo = request.GET.get("tipo")

        if not tipo:
            raise APIMissingSuaMesaType

        DAO = cls.switcher(tipo)
        return DAO.get(orgao_id, request)

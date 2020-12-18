"""
Módulo que define as funções usadas no switcher da classe SuaMesaDAO.

Cada novo tipo de caixinha do Sua Mesa deverá ter uma função associada, que
define as regras de negócio utilizadas na busca do resultado daquela caixinha.
"""

from dominio.models import Vista, Documento, SubAndamento
from dominio.pip.utils import get_orgaos_same_aisps
from dominio.suamesa.exceptions import APIMissingRequestParameterSuaMesa
from dominio.suamesa.helper import (
    TUTELA_INVESTIGACOES,
    TUTELA_PROCESSOS,
    TUTELA_FINALIZACOES,
    PIP_INQUERITOS,
    PIP_PICS,
    PIP_FINALIZACOES
)


def get_vistas(orgao_id, request):
    """Busca o número de vistas abertas de um CPF em um dado órgão."""
    cpf = request.GET.get("cpf")
    if not cpf:
        e = "Parâmetro 'cpf' não foi dado!"
        raise APIMissingRequestParameterSuaMesa(e)
    return Vista.vistas.abertas_promotor(orgao_id, cpf).count()


def get_tutela_investigacoes(orgao_id, request):
    """Busca o número de investigações ativas em uma tutela coletiva."""
    return Documento.investigacoes.em_curso(
        orgao_id,
        TUTELA_INVESTIGACOES,
        TUTELA_FINALIZACOES
    )


def get_tutela_processos(orgao_id, request):
    """Busca o número de processos ativos em uma tutela coletiva."""
    return Documento.processos.em_juizo(
        orgao_id,
        TUTELA_PROCESSOS,
        TUTELA_FINALIZACOES
    )


def get_pip_inqueritos(orgao_id, request):
    """Busca o número de inquéritos ativos em uma PIP."""
    return Documento.investigacoes.em_curso(
        orgao_id,
        PIP_INQUERITOS,
        PIP_FINALIZACOES
    )


def get_pip_pics(orgao_id, request):
    """Busca o número de PICs ativos em uma PIP."""
    return Documento.investigacoes.em_curso(
        orgao_id,
        PIP_PICS,
        PIP_FINALIZACOES
    )


def get_pip_aisp(orgao_id, request):
    """Busca o número de inquéritos e PICs ativos na AISP de uma PIP."""
    _, orgaos_same_aisp = get_orgaos_same_aisps(orgao_id)

    regras = PIP_INQUERITOS + PIP_PICS

    return Documento.investigacoes.em_curso_grupo(
        orgaos_same_aisp,
        regras,
        PIP_FINALIZACOES
    )


def get_tutela_finalizados(orgao_id, request):
    """Busca o número de documentos finalizados nos últimos 30 dias"""
    res = SubAndamento.finalizados.trinta_dias(
        orgao_id, TUTELA_FINALIZACOES).count()
    return res


def get_pip_finalizados(orgao_id, request):
    return SubAndamento.finalizados.trinta_dias(
        orgao_id, PIP_FINALIZACOES).count()

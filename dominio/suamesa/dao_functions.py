"""
Módulo que define as funções usadas no switcher da classe SuaMesaDAO.

Cada novo tipo de caixinha do Sua Mesa deverá ter uma função associada, que
define as regras de negócio utilizadas na busca do resultado daquela caixinha.
"""

from dominio.models import Vista, Documento, SubAndamento
from dominio.pip.utils import get_orgaos_same_aisps

from dominio.suamesa.exceptions import APIMissingRequestParameterSuaMesa


def get_vistas(orgao_id, request):
    """Busca o número de vistas abertas de um CPF em um dado órgão."""
    cpf = request.GET.get("cpf")
    if not cpf:
        e = "Parâmetro 'cpf' não foi dado!"
        raise APIMissingRequestParameterSuaMesa(e)
    return Vista.vistas.abertas_promotor(orgao_id, cpf).count()


def get_tutela_investigacoes(orgao_id, request):
    """Busca o número de investigações ativas em uma tutela coletiva."""
    regras = [
        51219, 51220, 51221, 51222, 51223,  # Procedimentos Administrativos
        392,                                # Inquérito Civil
        395                                 # Procedimento Preparatório
    ]
    return Documento.investigacoes.em_curso(orgao_id, regras)


def get_tutela_processos(orgao_id, request):
    """Busca o número de processos ativos em uma tutela coletiva."""
    regras = [
        441, 177,                 # Ação Civil Pública
        175,                      # Ação Civil Coletiva
        176, 127,                 # Ação de Improbidade Administrativa
        18, 126, 159,             # Ação Rescisória
        320,                      # Execução de TAC
        582, 323,                 # Execução Provisória
        319, 51218, 51217, 51205  # Execução Extrajudicial
    ]
    return Documento.processos.em_juizo(orgao_id, regras)


def get_pip_inqueritos(orgao_id, request):
    """Busca o número de inquéritos ativos em uma PIP."""
    regras = [494, 3]  # Inquérito Policial, e Policial Militar em ordem
    return Documento.investigacoes.em_curso(orgao_id, regras)


def get_pip_pics(orgao_id, request):
    """Busca o número de PICs ativos em uma PIP."""
    regras = [590]  # Procedimento Investigatório Criminal (PIC)
    return Documento.investigacoes.em_curso(orgao_id, regras)


def get_pip_aisp(orgao_id, request):
    """Busca o número de inquéritos e PICs ativos na AISP de uma PIP."""
    _, orgaos_same_aisp = get_orgaos_same_aisps(orgao_id)

    # Inquéritos Policiais, Policiais Militares, e PICs
    regras = [494, 3, 590]

    return Documento.investigacoes.em_curso_grupo(
        orgaos_same_aisp, regras
    )


def get_tutela_finalizados(orgao_id, request):
    """
    Busca o número de documentos finalizados nos últimos 30 dias, ou seja, que
    tiveram algum dos movimentos finalizadores definidos nesta função.
    """
    regras_ajuizamento = (6251, )
    regras_tac = (6655, 6326)
    regras_arquiv = (7912, 6548, 6326, 6681, 6678, 6645, 6682, 6680, 6679,
                     6644, 6668, 6666, 6665, 6669, 6667, 6664, 6655, 6662,
                     6659, 6658, 6663, 6661, 6660, 6657, 6670, 6676, 6674,
                     6673, 6677, 6675, 6672, 6018, 6341, 6338, 6019, 6017,
                     6591, 6339, 6553, 7871, 6343, 6340, 6342, 6021, 6334,
                     6331, 6022, 6020, 6593, 6332, 7872, 6336, 6333, 6335,
                     7745, 6346, 6345, 6015, 6016, 6325, 6327, 6328, 6329,
                     6330, 6337, 6344, 6656, 6671, 7869, 7870, 6324, 7834,
                     7737, 6350)

    # Desarquivamentos servem pra anular qualquer das regras anteriores
    # regras_desarq = (6075, 1028, 6798, 7245, 6307, 1027, 7803, 6003, 7802,
    #                  7801, 6004, 6696)

    regras = regras_ajuizamento + regras_tac + regras_arquiv  # +regras_desarq

    res = SubAndamento.finalizados.trinta_dias(
        orgao_id, regras).count()
    return res


def get_pip_finalizados(orgao_id, request):
    regras_arquiv = (6682, 6669, 6018, 6341, 6338, 6019, 6017, 6591, 6339,
                     7871, 6343, 6340, 6342, 7745, 6346, 7915, 6272, 6253,
                     6392, 6377, 6378, 6359, 6362, 6361, 6436, 6524, 7737,
                     7811, 6625, 6718, 7834, 6350)

    # Os mesmos desarquivamentos de Tutela servem para PIP
    # regras_desarq = (6075, 1028, 6798, 7245, 6307, 1027, 7803, 6003, 7802,
    #                  7801, 6004, 6696)
    regras = regras_arquiv  # +regras_desarq

    return SubAndamento.finalizados.trinta_dias(
        orgao_id, regras).count()

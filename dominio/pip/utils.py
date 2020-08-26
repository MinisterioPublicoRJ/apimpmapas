from functools import lru_cache

from django.conf import settings

from dominio.db_connectors import run_query
from dominio.utils import get_top_n_orderby_value_as_dict


@lru_cache()
def get_aisps():
    """Retorna as AISPs de cada PIP, na seguinte ordem:
    (codigo_pip, codigo_aisp, nome_aisp)
    """
    query = """
        SELECT pip_codigo, aisp_codigo, aisp_nome, cod_pct 
        FROM {namespace}.tb_pip_aisp
        JOIN {namespace}.atualizacao_pj_pacote ON pip_codigo = id_orgao
    """.format(
        namespace=settings.TABLE_NAMESPACE
    )
    return run_query(query)

def get_orgaos_same_aisps(orgao_id):
    """Retorna os órgãos que pertencem às mesmas AISPs de orgao_id, por AISP.

    Arguments:
        orgao_id {int} -- ID do órgão a filtrar.

    Returns:
        list(dict) -- Lista de dicionários contendo o número da AISP e .
    """
    data = get_aisps()
    cod_pct_current_orgao = [x[3] for x in data if x[0] == orgao_id][0]
    aisps_current_orgao = set(x[1] for x in data if x[0] == orgao_id)
    orgaos_same_aisps = set(
        x[0] for x in data
        if x[1] in aisps_current_orgao and x[3] == cod_pct_current_orgao)

    return aisps_current_orgao, orgaos_same_aisps


def get_top_n_by_aisp(orgaos_same_aisps, data, **kwargs):
    """Ordena uma lista de tuplas utilizando uma posição escolhida,
    e retorna os top N maiores em um formato de lista de dicionários
    com um campo de nome e um campo de valor, para cada AISP dada.

    Arguments:
        orgaos_same_aisps {dict} --Lista de órgãos por AISP a ser considerada.
        data {list} -- Dados que devem ser mostradas para os órgãos.
        name_position {int} --Posição da tupla onde está o nome da promotoria.
        value_position {int} -- Posição da tupla onde está o valor usado
            para ordenação.
        name_fieldname {string} -- Nome do campo de nome presente nos
            dicionários finais.
        value_fieldname {string} -- Nome do campo de valor presente nos
            dicionários finais.

    Keyword Arguments:
        n {int} -- Quantidade de dados a retornar no Top N.

    Returns:
        List[dict] -- Lista de dicionários contendo os Top N em ordem.
    """
    mapping_orgao_to_data = {x[0]: x for x in data}

    return get_top_n_orderby_value_as_dict(
        [mapping_orgao_to_data[orgao] for orgao in orgaos_same_aisps], **kwargs
    )

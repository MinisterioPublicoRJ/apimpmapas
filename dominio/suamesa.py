from functools import lru_cache

from decouple import config
from django.conf import settings

from .db_connectors import run_query


QUERY_REGRAS = """
    SELECT r.classe_documento
    FROM {namespace}.atualizacao_pj_pacote pct
    JOIN {namespace}.{regras_table} r
    ON r.cod_atribuicao = pct.cod_pct
    WHERE pct.id_orgao = :orgao_id
    """


VISTAS_PAGE_SIZE = config('VISTAS_PAGE_SIZE', cast=int, default=20)


def format_text(text):
    return ' '.join(
        [t.capitalize() if len(t) > 3 else t for t in text.lower().split()]
    )


@lru_cache()
def get_regras(orgao_id, tipo='investigacao'):
    """Busca as regras de negócio relativas a investigação ou processo,
    para um dado órgão.

    Arguments:
        orgao_id {integer} -- ID do órgão a ser procurado.

    Keyword Arguments:
        tipo {str} -- Tipo de regra a ser procurada.
        Pode ser 'investigacao' ou 'processo'. (default: {'investigacao'})

    Returns:
        List[integer] -- Lista de IDs de classes de documentos.
    """
    table_switcher = {
        'investigacao': 'tb_regra_negocio_investigacao',
        'processo': 'tb_regra_negocio_processo'
    }
    regras_table = table_switcher.get(tipo, None)

    if not regras_table:
        # Melhor fazer de outra forma? Raise error?
        return None

    query = QUERY_REGRAS.format(
        regras_table=regras_table,
        namespace=settings.TABLE_NAMESPACE
    )
    parameters = {
        'orgao_id': orgao_id
    }

    result = run_query(query, parameters)
    return [row[0] for row in result] if result else []

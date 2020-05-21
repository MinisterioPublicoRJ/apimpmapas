"""
Definição do DAO (Data Access Object) usado pela View do SuaMesa.

Este DAO irá pegar o tipo de dado a ser buscado (especificado no request),
e irá chamar a função apropriada para fazer esta busca.

Caso o tipo de dado não seja especificado, ou seja informado um tipo de dado
não definido, o DAO irá levantar uma exceção.
"""

from dominio.suamesa.exceptions import (
    APIInvalidSuaMesaType,
    APIMissingSuaMesaType,
)
from dominio.suamesa.dao_functions import (
    get_vistas,
    get_tutela_investigacoes,
    get_tutela_processos,
    get_pip_inqueritos,
    get_pip_pics,
    get_pip_aisp,
    get_finalizados
)


class SuaMesaDAO:
    _type_switcher = {
        'vistas': get_vistas,
        'tutela_investigacoes': get_tutela_investigacoes,
        'tutela_processos': get_tutela_processos,
        'pip_inqueritos': get_pip_inqueritos,
        'pip_pics': get_pip_pics,
        'pip_aisp': get_pip_aisp,
        'tutela_finalizados': get_finalizados
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

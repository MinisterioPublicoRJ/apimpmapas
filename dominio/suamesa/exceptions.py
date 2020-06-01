"""
Exceptions específicas do DAO do SuaMesa ou das funções associadas.
"""

from rest_framework.exceptions import APIException


class APIInvalidSuaMesaType(APIException):
    status_code = 404
    default_detail = "SuaMesa recebeu um tipo sem função definida!"
    default_code = "api_suamesa_invalid_type"


class APIMissingSuaMesaType(APIException):
    status_code = 400
    default_detail = "SuaMesa não recebeu o parâmetro 'tipo'!"
    default_code = "api_suamesa_missing_type_parameter"


class APIMissingRequestParameterSuaMesa(APIException):
    status_code = 400
    default_detail = ("SuaMesa não recebeu um parâmetro "
                      "obrigatório para a função escolhida!")
    default_code = "api_suamesa_missing_required_parameter_for_type"

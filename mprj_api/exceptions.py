from rest_framework.exceptions import APIException


class APIQueryError(APIException):
    status_code = 500
    default_detail = "Erro durante execução da query"
    default_code = "api_query_error"


class APIEmptyResultError(APIException):
    status_code = 404
    default_detail = "Result set retornou vazio"
    default_code = "api_empty_result_error"

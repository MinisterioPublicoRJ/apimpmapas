from rest_framework.exceptions import APIException


class APIEmptyResultError(APIException):
    status_code = 404
    default_detail = "Result set retornou vazio"
    default_code = "api_empty_result_error"


class UserHasNoValidOfficesError(APIException):
    status_code = 404
    default_detail = "Usário não está lotado em órgãos válidos"
    default_code = "invalid_offices_errors"

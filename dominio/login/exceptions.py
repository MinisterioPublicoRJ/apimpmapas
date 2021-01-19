from rest_framework.exceptions import APIException


class UserHasNoValidOfficesError(APIException):
    status_code = 404
    default_detail = "Usuário não está lotado em órgãos válidos"
    default_code = "invalid_offices_errors"


class UserDetailsNotFoundError(APIException):
    status_code = 404
    default_detail = "Resultado da query no MGP não retornou dados do usuário"
    default_code = "user_data_not_found"


class UserHasNoOfficeInformation(APIException):
    status_code = 404
    default_detail = "Não foram encontrados órgãos para este usuário"
    default_code = "no_office_found"

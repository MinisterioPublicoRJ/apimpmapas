from rest_framework.exceptions import APIException


class ServiceUnavailable(APIException):
    status_code = 503
    default_detail = (
        "Ocorreu um erro no serviço. Por favor, verifique os parâmetros da"
        " requisição ou tente novamente mais tarde"
    )
    default_code = "solr_placas_service_unavailable"

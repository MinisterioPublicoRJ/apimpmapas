from rest_framework.exceptions import APIException


class APIInvalidOverlayType(APIException):
    status_code = 404
    default_detail = "Alerta Overlay recebeu um tipo sem função definida!"
    default_code = "api_alerta_overlay_invalid_type"


class APIMissingOverlayType(APIException):
    status_code = 400
    default_detail = "Alerta Overlay não recebeu o parâmetro 'tipo'!"
    default_code = "api_alerta_overlay_missing_type_parameter"


class APIMissingRequestParameterOverlay(APIException):
    status_code = 400
    default_detail = ("Alerta Overlay não recebeu um parâmetro "
                      "obrigatório para a função escolhida!")
    default_code = "api_alerta_overlay_missing_required_parameter_for_type"


class APIAlertTypeListNotConfigured(APIException):
    status_code = 404
    default_detail = ("O parâmetro tipo_alerta recebido não está "
                      "configurado para retornar lista!")
    default_code = "api_alert_type_list_not_configured"

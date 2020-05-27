from rest_framework.exceptions import APIException


# TODO: mover essas excessões para o módulo que pertencem
class DataDoesNotExistException(Exception):
    pass


class WaitDBException(Exception):
    pass


class DetranAPIClientError(Exception):
    pass


class ServiceUnavailableAPIException(APIException):
    status_code = 503

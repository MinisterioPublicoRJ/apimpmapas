from time import sleep

from decouple import config
from zeep import Client

from proxies.exceptions import DetranCustonError

CNPJ = config('CNPJ')
CHAVE = config('CHAVE')
PERFIL = config('PERFIL')
CPF = config('CPF')
URL_DETRAN_ENVIO = config('URL_DETRAN_ENVIO')
URL_DETRAN_BUSCA = config('URL_DETRAN_BUSCA')


def request_data(rg, max_attempts=3, waiting_time=3):

    search_connector = Client(URL_DETRAN_ENVIO)
    result_connector = Client(URL_DETRAN_BUSCA)

    search_connector.service.consultarRG(
        CNPJ,
        CHAVE,
        PERFIL,
        rg,
        rg.zfill(10),
        CPF)

    attempt = 0
    return_message = None

    while (attempt <= max_attempts and return_message) is None:

        attempt += 1

        sleep(waiting_time)

        result = result_connector.service.BuscarProcessados(
            CNPJ, CHAVE, PERFIL, rg)

        if result is not None:

            return_message = result[0].MsgRetorno

            try:
                photo = result[0].fotoCivil.string[0]

            except AttributeError as Error:
                raise DetranCustonError(return_message)

        else:
            raise DetranCustonError("Não foi possível acessar a API do Detran")

    return photo

from time import sleep

from decouple import config
from zeep import Client

from proxies.exceptions import DetranAPIClientError

CNPJ = config("CNPJ")
CHAVE = config("CHAVE")
PERFIL = config("PERFIL")
CPF = config("CPF")
URL_DETRAN_ENVIO = config("URL_DETRAN_ENVIO")
URL_DETRAN_BUSCA = config("URL_DETRAN_BUSCA")


def request_data(rg, max_attempts=3, waiting_time=3):

    search_connector = Client(URL_DETRAN_ENVIO)
    result_connector = Client(URL_DETRAN_BUSCA)

    search_connector.service.consultarRG(
        CNPJ, CHAVE, PERFIL, rg, rg.zfill(10), CPF
    )

    attempt = 0
    return_message = None

    result = result_connector.service.BuscarProcessados(
        CNPJ, CHAVE, PERFIL, rg
    )

    return result[0].fotoCivil.string[0]

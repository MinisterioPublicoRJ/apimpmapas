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

    result = result_connector.service.BuscarProcessados(
        CNPJ, CHAVE, PERFIL, rg
    )
    attempts = 1
    while result is None and attempts < max_attempts:
        try:
            result = result_connector.service.BuscarProcessados(
                CNPJ, CHAVE, PERFIL, rg
            )
        except:
            # TODO: encontrar as excessões possíveis
            pass

        attempts += 1


    return result[0].fotoCivil.string[0]

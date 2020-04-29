from decouple import config
from zeep import Client

from proxies.exceptions import DetranAPIClientError

CNPJ = config("CNPJ")
CHAVE = config("CHAVE")
PERFIL = config("PERFIL")
CPF = config("CPF")
URL_DETRAN_ENVIO = config("URL_DETRAN_ENVIO")
URL_DETRAN_BUSCA = config("URL_DETRAN_BUSCA")


def request_data(rg):
    search_connector = Client(URL_DETRAN_ENVIO)
    result_connector = Client(URL_DETRAN_BUSCA)

    search_connector.service.consultarRG(
        CNPJ, CHAVE, PERFIL, rg, rg.zfill(10), CPF
    )

    result = result_connector.service.BuscarProcessados(
        CNPJ, CHAVE, PERFIL, rg
    )

    if result[0].RG is None:
        raise DetranAPIClientError(
            "Não foi possível buscar a foto na API do Detran"
        )

    return result[0].fotoCivil.string[0]

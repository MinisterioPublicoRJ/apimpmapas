from django.conf import settings
from zeep import Client

from proxies.exceptions import DetranAPIClientError


def request_data(rg):
    search_connector = Client(settings.DETRAN_URL_ENVIO)
    result_connector = Client(settings.DETRAN_URL_BUSCA)

    search_connector.service.consultarRG(
        settings.DETRAN_CNPJ,
        settings.DETRAN_CHAVE,
        settings.DETRAN_PERFIL,
        rg,
        rg.zfill(10),
        settings.DETRAN_CPF
    )

    result = result_connector.service.BuscarProcessados(
        settings.DETRAN_CNPJ, settings.DETRAN_CHAVE, settings.DETRAN_PERFIL, rg
    )

    if result[0].RG is None:
        raise DetranAPIClientError(
            "Não foi possível buscar a foto na API do Detran"
        )

    return result[0].fotoCivil.string[0]

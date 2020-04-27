from unittest import mock

from decouple import config

from proxies.detran.client import request_data


@mock.patch("proxies.detran.client.Client")
def test_get_photo_rg_sucess_no_retry(_Client):
    mock_send = mock.Mock()
    mock_retrieve = mock.Mock()
    api_response = [mock.Mock(fotoCivil=mock.Mock(string=["photo"]))]
    mock_retrieve.service.BuscarProcessados.return_value = api_response

    _Client.side_effect = [mock_send, mock_retrieve]


    rg = "12345"
    photo = request_data(rg)
    expected = "ThisIsAPhoto,TrustMe"

    _Client.assert_has_calls(
        [
            mock.call(config("URL_DETRAN_ENVIO")),
            mock.call(config("URL_DETRAN_BUSCA")),
        ]
    )

    mock_send.service.consultarRG(
        config("CNPJ"),
        config("CHAVE"),
        config("PERFIL"),
        rg.zfill(10),
        config("CPF"),
    )
    mock_retrieve.service.BuscarProcessados.assert_called_once_with(
        config("CNPJ"),
        config("CHAVE"),
        config("PERFIL"),
        rg,
    )
    assert photo == "photo"

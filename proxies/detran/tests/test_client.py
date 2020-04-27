from unittest import mock

import pytest
from decouple import config

from proxies.exceptions import DetranAPIClientError
from proxies.detran.client import request_data

class TestDetranAPIClient:
    @mock.patch("proxies.detran.client.Client")
    def test_get_photo_rg_sucess_no_retry(self, _Client):
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

    @mock.patch("proxies.detran.client.Client")
    def test_get_photo_rg_sucess_with_retry(self, _Client):
        mock_send = mock.Mock()
        mock_retrieve = mock.Mock()
        api_response = [
            None,
            None,
            [mock.Mock(fotoCivil=mock.Mock(string=["photo"]))],
        ]
        mock_retrieve.service.BuscarProcessados.side_effect = api_response

        _Client.side_effect = [mock_send, mock_retrieve]


        rg = "12345"
        photo = request_data(rg)
        expected  = "photo"

        assert photo == expected

    @mock.patch("proxies.detran.client.Client")
    def test_get_photo_rg_sucess_with_retry_api_exception(self, _Client):
        mock_send = mock.Mock()
        mock_retrieve = mock.Mock()
        api_response = [
            None,
            Exception,
            [mock.Mock(fotoCivil=mock.Mock(string=["photo"]))],
        ]
        mock_retrieve.service.BuscarProcessados.side_effect = api_response

        _Client.side_effect = [mock_send, mock_retrieve]


        rg = "12345"
        photo = request_data(rg)
        expected  = "photo"

        assert photo == expected

    @mock.patch("proxies.detran.client.Client")
    def test_get_photo_rg_fail(self, _Client):
        mock_send = mock.Mock()
        mock_retrieve = mock.Mock()
        api_response = [
            None,
            Exception,
            Exception,
        ]
        mock_retrieve.service.BuscarProcessados.side_effect = api_response

        _Client.side_effect = [mock_send, mock_retrieve]


        rg = "12345"
        with pytest.raises(DetranAPIClientError):
            request_data(rg)

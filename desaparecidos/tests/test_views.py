from unittest import mock

from django.test import TestCase
from django.urls import reverse

from desaparecidos import settings as d_settings


class Desaparecidos(TestCase):
    @mock.patch("desaparecidos.views.rank")
    @mock.patch("desaparecidos.views.client")
    def test_correct_response(self, _client, _rank):
        _client.return_value = "cursor"
        _rank.return_value = {"result": "1234"}

        url = reverse('desaparecidos:busca', kwargs={"id_sinalid": "1234"})

        resp = self.client.get(url)

        _client.assert_called_once_with(
            d_settings.DESAPARECIDOS_DB_USER,
            d_settings.DESAPARECIDOS_DB_PWD,
            d_settings.DESAPARECIDOS_DB_HOST
        )
        _rank.assert_called_once_with("cursor", "1234")
        self.assertEqual(resp.status_code, 200)

    @mock.patch("desaparecidos.views.rank")
    @mock.patch("desaparecidos.views.client")
    def test_erro_response(self, _client, _rank):
        _client.return_value = "cursor"
        _rank.return_value = {"erro": "ID Sinalid não encontrado"}

        url = reverse('desaparecidos:busca', kwargs={"id_sinalid": "xxxx"})

        resp = self.client.get(url)

        _client.assert_called_once_with(
            d_settings.DESAPARECIDOS_DB_USER,
            d_settings.DESAPARECIDOS_DB_PWD,
            d_settings.DESAPARECIDOS_DB_HOST
        )
        _rank.assert_called_once_with("cursor", "xxxx")
        self.assertEqual(resp.status_code, 404)

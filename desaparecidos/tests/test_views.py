from unittest import mock

from django.test import TestCase
from django.urls import reverse


class Desaparecidos(TestCase):
    @mock.patch("desaparecidos.views.rank")
    def test_correct_response(self, _rank):
        _rank.return_value = [{"result": "1234"}]

        url = reverse('desaparecidos:busca', kwargs={"id_sinalid": "1234"})

        resp = self.client.get(url)

        _rank.assert_called_once_with("1234")
        self.assertEqual(resp.status_code, 200)

    @mock.patch("desaparecidos.views.rank")
    def test_erro_response(self, _rank):
        _rank.return_value = {"erro": "ID Sinalid não encontrado"}

        url = reverse('desaparecidos:busca', kwargs={"id_sinalid": "xxxx"})

        resp = self.client.get(url)
        _rank.assert_called_once_with("xxxx")
        self.assertEqual(resp.status_code, 404)

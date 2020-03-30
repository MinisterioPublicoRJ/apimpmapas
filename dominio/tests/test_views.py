from datetime import date
from unittest import mock

import pytest
from django.test import TestCase
from django.urls import reverse
from freezegun import freeze_time
from model_bakery.baker import make

from dominio.tests.testconf import NoJWTTestCase


@pytest.mark.django_db(transaction=True)
class TestLogin(TestCase):
    @mock.patch("dominio.views.authenticate_integra")
    def test_correct_response(self, _auth_integra):
        _auth_integra.return_value = {"username": "username"}
        url = reverse("dominio:login")

        resp = self.client.post(url)
        expected_data = {
            "first_login": True,
            "first_login_today": True,
            "username": "username",
        }

        self.assertEqual(resp.status_code, 200)
        _auth_integra.assert_called()
        self.assertEqual(resp.json(), expected_data)

    @freeze_time('2020-01-01')
    @mock.patch("dominio.views.authenticate_integra")
    def test_user_already_logged_in(self, _auth_integra):
        _auth_integra.return_value = {"username": "username"}
        url = reverse("dominio:login")

        make("dominio.Usuario", username="username")

        with mock.patch("dominio.models.date") as date_mock:
            date_mock.today.return_value = date(2020, 1, 2)
            resp = self.client.post(url)
        expected_data = {
            "first_login": False,
            "first_login_today": True,
            "username": "username",
        }

        self.assertEqual(resp.status_code, 200)
        _auth_integra.assert_called()
        self.assertEqual(resp.json(), expected_data)

    @freeze_time('2020-01-01')
    @mock.patch("dominio.views.authenticate_integra")
    def test_user_already_logged_in_today(self, _auth_integra):
        _auth_integra.return_value = {"username": "username"}
        url = reverse("dominio:login")

        make("dominio.Usuario", username="username")

        with mock.patch("dominio.models.date") as date_mock:
            date_mock.today.return_value = date(2020, 1, 1)
            resp = self.client.post(url)
        expected_data = {
            "first_login": False,
            "first_login_today": False,
            "username": "username",
        }

        self.assertEqual(resp.status_code, 200)
        _auth_integra.assert_called()
        self.assertEqual(resp.json(), expected_data)


class TestTempoTramitacao(NoJWTTestCase, TestCase):
    @mock.patch('dominio.views.run_query')
    def test_correct_response(self, _run_query):
        expected = {
            "id_orgao": 12345,
            "media_orgao": 10.1243,
            "minimo_orgao": 0,
            "maximo_orgao": 100,
            "mediana_orgao": 10.2312,
            "media_pacote": 11.4352,
            "minimo_pacote": 0,
            "maximo_pacote": 200,
            "mediana_pacote": 56.3124,
            "media_pacote_t1": 45.343,
            "minimo_pacote_t1": 12,
            "maximo_pacote_t1": 533,
            "mediana_pacote_t1": 343.324,
            "media_orgao_t1": 344.12,
            "minimo_orgao_t1": 12,
            "maximo_orgao_t1": 5023,
            "mediana_orgao_t1": 2421.1223,
            "media_pacote_t2": 343.1254,
            "minimo_pacote_t2": 48,
            "maximo_pacote_t2": 2335,
            "mediana_pacote_t2": 7623.1224,
            "media_orgao_t2": 43224.1132,
            "minimo_orgao_t2": 432,
            "maximo_orgao_t2": 1324,
            "mediana_orgao_t2": 2242.3232
        }
        _run_query.return_value = [expected.values()]
        url = reverse("dominio:tempo-tramitacao", args=("1234", ))
        resp = self.client.get(url)

        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.data, expected)


class TestNumeroDesarquivamentos(NoJWTTestCase, TestCase):
    @mock.patch("dominio.views.connections")
    def test_correct_response(self, _connections):
        cursor_mock = mock.MagicMock()
        cursor_mock.execute.return_value.fetchall.return_value\
            = [("nr_mp_1", 1), ("nr_mp_2", 2)]
        conn_mock = mock.MagicMock()
        conn_mock.cursor.return_value.__enter__.return_value = cursor_mock

        _connections.__getitem__.return_value = conn_mock
        url = reverse("dominio:desarquivamentos", args=("12345",))

        resp = self.client.get(url)
        expected = [
            {"numero_mprj": "nr_mp_1", "qtd_desarq": 1},
            {"numero_mprj": "nr_mp_2", "qtd_desarq": 2},
        ]

        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.data, expected)

from datetime import datetime, timedelta
from decimal import Decimal
from unittest import mock

from django.conf import settings
from django.test import TestCase
from django.urls import reverse

from dominio.tutela.views import RadarView
from dominio.tests.testconf import NoJWTTestCase, NoCacheTestCase


class OutliersViewTest(NoJWTTestCase, NoCacheTestCase, TestCase):
    @mock.patch('dominio.tutela.views.OutliersDAO.get')
    def test_outliers_result(self, _get_data):
        _get_data.return_value = [{"data": 1}]

        response = self.client.get(reverse(
            'dominio:outliers',
            args=('0')))

        _get_data.assert_called_once_with(orgao_id=0)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, [{"data": 1}])


class SaidasViewTest(NoJWTTestCase, NoCacheTestCase, TestCase):
    @mock.patch('dominio.tutela.views.SaidasDAO.get')
    def test_saidas_result(self, _get_data):
        _get_data.return_value = [{"data": 1}]

        response = self.client.get(reverse(
            'dominio:saidas',
            args=('120',)))

        _get_data.assert_called_once_with(orgao_id=120)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, [{"data": 1}])


class EntradasViewTest(NoJWTTestCase, NoCacheTestCase, TestCase):
    @mock.patch('dominio.tutela.views.EntradasDAO.get')
    def test_entradas_result(self, _get_data):
        _get_data.return_value = [{"data": 1}]

        response = self.client.get(reverse(
            'dominio:entradas',
            args=('1', '2')))

        _get_data.assert_called_once_with(orgao_id=1, nr_cpf='2')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, [{"data": 1}])


class ListaProcessosViewTest(NoJWTTestCase, NoCacheTestCase, TestCase):
    @mock.patch('dominio.tutela.views.ListaProcessosView.PROCESSOS_SIZE')
    @mock.patch('dominio.tutela.views.ListaProcessosDAO.get')
    def test_lista_processos_result(self, _get_data, _PROCESSOS_SIZE):
        _PROCESSOS_SIZE.return_value = 1
        _get_data.return_value = [{"data": 1}, {"data": 2}, {"data": 3}]

        response_1 = self.client.get(reverse(
            'dominio:lista-processos',
            args=('1')) + '?page=1')
        response_2 = self.client.get(reverse(
            'dominio:lista-processos',
            args=('1')) + '?page=2')

        expected_response_page_1 = [{"data": 1}]
        expected_response_page_2 = [{"data": 2}]

        _get_data.assert_called_with(orgao_id=1)
        self.assertEqual(response_1.status_code, 200)
        self.assertEqual(response_2.status_code, 200)
        self.assertEqual(response_1.data, expected_response_page_1)
        self.assertEqual(response_2.data, expected_response_page_2)


class TestTempoTramitacao(NoJWTTestCase, TestCase):
    @mock.patch('dominio.tutela.dao.TempoTramitacaoDAO.get')
    def test_correct_response(self, _get_data):
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
        _get_data.return_value = expected
        url = reverse("dominio:tempo-tramitacao", args=("1234", ))
        resp = self.client.get(url)

        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.data, expected)

    @mock.patch('dominio.tutela.dao.TempoTramitacaoIntegradoDAO.get')
    def test_correct_response_v11(self, _get_data):
        expected = {
            "id_orgao": 1234,
            "tp_tempo": 'tipo',
            "media_orgao": 12.34,
            "minimo_orgao": 12.34,
            "maximo_orgao": 12.34,
            "mediana_orgao": 12.34,
            "media_pacote": 12.34,
            "minimo_pacote": 12.34,
            "maximo_pacote": 12.34,
            "mediana_pacote": 12.34
        }
        _get_data.return_value = expected
        url = reverse("dominio:tempo-tramitacao", args=("1234", ))
        resp = self.client.get(url, data={'version': '1.1'})

        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.data, expected)


class TestNumeroDesarquivamentos(NoJWTTestCase, TestCase):
    @mock.patch("dominio.tutela.views.connections")
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


class TestComparadorRadares(NoJWTTestCase, TestCase):
    @mock.patch("dominio.tutela.views.ComparadorRadaresDAO.execute")
    def test_correct_response(self, _execute):
        _execute.return_value = [
            (
                "3456",
                "2ª PJ",
                "2ª PROMOTORIA",
                1.0,
                0.0,
                None,
                0.7,
                None
            ),
            (
                "6789",
                "1ª PJ",
                "1ª PROMOTORIA",
                1.0,
                1.0,
                None,
                1.0,
                None
            )
        ]
        url = reverse("dominio:tutela-comparador-radares", args=("12345",))
        resp = self.client.get(url)
        expected_data = [
            {
                "orgao_id": "3456",
                "orgao_codamp": "2ª PJ",
                "orgi_nm_orgao": "2ª PROMOTORIA",
                "perc_arquivamentos": 1.0,
                "perc_indeferimentos": 0.0,
                "perc_instauracoes": None,
                "perc_tac": 0.7,
                "perc_acoes": None
            },
            {
                "orgao_id": "6789",
                "orgao_codamp": "1ª PJ",
                "orgi_nm_orgao": "1ª PROMOTORIA",
                "perc_arquivamentos": 1.0,
                "perc_indeferimentos": 1.0,
                "perc_instauracoes": None,
                "perc_tac": 1.0,
                "perc_acoes": None
            }
        ]

        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.data, expected_data)


class TestRadarPromotoria(NoJWTTestCase, NoCacheTestCase, TestCase):
    @mock.patch("dominio.tutela.views.RadarPerformanceDAO.get")
    def test_correct_response(self, _get):
        _get.return_value = [{"data": 1}]

        url = reverse(
            "dominio:radar",
            args=("1234",)
        )
        resp = self.client.get(url)

        _get.assert_called_once_with(orgao_id=1234)
        assert resp.status_code == 200
        assert resp.data == [{"data": 1}]

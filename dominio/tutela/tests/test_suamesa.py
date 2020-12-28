from datetime import date
from unittest import mock

from django.conf import settings
from django.urls import reverse
from django.test import TestCase

from dominio.tutela.suamesa import (
    get_regras,
    QUERY_REGRAS,
    VISTAS_PAGE_SIZE,
)

from dominio.tests.testconf import NoJWTTestCase, NoCacheTestCase


class TestSuaMesa(TestCase):
    @mock.patch('dominio.tutela.suamesa.run_query')
    def test_sua_mesa_get_regras_investigacao(self, _run_query):
        _run_query.return_value = [(20,), (30,)]

        orgao_id = 10
        output = get_regras(orgao_id, 'investigacao')
        expected_output = [20, 30]

        expected_query = QUERY_REGRAS.format(
            regras_table="tb_regra_negocio_investigacao",
            namespace=settings.TABLE_NAMESPACE
        )
        expected_parameters = {
            'orgao_id': orgao_id
        }

        _run_query.assert_called_once_with(expected_query, expected_parameters)
        self.assertEqual(output, expected_output)

    @mock.patch('dominio.tutela.suamesa.run_query')
    def test_sua_mesa_get_regras_processo(self, _run_query):
        _run_query.return_value = [(20,), (30,)]

        orgao_id = 10
        output = get_regras(orgao_id, 'processo')
        expected_output = [20, 30]

        expected_query = QUERY_REGRAS.format(
            regras_table="tb_regra_negocio_processo",
            namespace=settings.TABLE_NAMESPACE
        )
        expected_parameters = {
            'orgao_id': orgao_id
        }

        _run_query.assert_called_once_with(expected_query, expected_parameters)
        self.assertEqual(output, expected_output)


class TestSuaMesaDetalheVistas(NoJWTTestCase, NoCacheTestCase, TestCase):
    @mock.patch('dominio.tutela.views.Vista')
    def test_correct_response(self, _Vista):
        expected_resp = {
            'soma_ate_vinte': 25,
            'soma_vinte_trinta': 2,
            'soma_trinta_mais': 4
        }
        _Vista.vistas.agg_abertas_por_data.return_value = expected_resp

        url = reverse('dominio:suamesa-detalhe-vistas', args=('1', '2'))

        resp = self.client.get(url)

        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.data, expected_resp)

    @mock.patch('dominio.tutela.views.Vista')
    def test_404_response(self, _Vista):
        query_resp = {
            'soma_ate_vinte': None,
            'soma_vinte_trinta': None,
            'soma_trinta_mais': None
        }
        _Vista.vistas.agg_abertas_por_data.return_value = query_resp

        url = reverse('dominio:suamesa-detalhe-vistas', args=('1', '2'))

        resp = self.client.get(url)

        self.assertEqual(resp.status_code, 404)


class TestSuaMesaListaVistasAbertas(NoJWTTestCase, NoCacheTestCase, TestCase):
    @mock.patch('dominio.tutela.views.Vista')
    def test_correct_response(self, _Vista):
        response = [
            {
                "numero_mprj": "1234",
                "numero_externo": "tj1234",
                "dt_abertura": date(2020, 1, 1),
                "classe": "classe 1",
                "docu_dk": "1"
            },
            {
                "numero_mprj": "9012",
                "numero_externo": "tj9012",
                "dt_abertura": date(2018, 1, 1),
                "classe": "classe 3",
                "docu_dk": "2"
            },
        ]
        _Vista.vistas.abertas_por_data.return_value = response

        expected = [
            {
                "numero_mprj": "1234",
                "numero_externo": "tj1234",
                "dt_abertura": '2020-01-01',
                "classe": "classe 1",
            },
            {
                "numero_mprj": "9012",
                "numero_externo": "tj9012",
                "dt_abertura": '2018-01-01',
                "classe": "classe 3",
            },
        ]
        url = reverse(
            'dominio:suamesa-lista-vistas',
            args=('1', '2', "trinta_mais")
        )
        url += '?page=1'

        resp = self.client.get(url)

        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.data, expected)

    def test_return_404_for_incorrcect_data_abertura_value(self):
        url = reverse(
            'dominio:suamesa-lista-vistas',
            args=('1', '2', "invalid")
        )

        resp = self.client.get(url)
        expected_msg = "data_abertura inválida. Opções são: ate_vinte, "\
            "vinte_trinta, trinta_mais"

        self.assertEqual(resp.status_code, 404)
        self.assertEqual(resp.data, expected_msg)

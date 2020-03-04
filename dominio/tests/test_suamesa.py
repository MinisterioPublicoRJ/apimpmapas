from datetime import date
from unittest import mock

from django.conf import settings
from django.core.cache import cache
from django.urls import reverse
from django.test import TestCase

from dominio.suamesa import get_regras, QUERY_REGRAS


class NoCacheTestCase:
    def tearDown(self):
        cache.clear()


class TestSuaMesa(TestCase):
    @mock.patch('dominio.suamesa.run_query')
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

    @mock.patch('dominio.suamesa.run_query')
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


class SuaMesaViewTest(TestCase, NoCacheTestCase):
    @mock.patch('dominio.views.suamesa.get_regras')
    @mock.patch('dominio.views.Documento')
    def test_sua_mesa_investigacoes(self, _Documento, _get_regras):
        manager_mock = mock.MagicMock()
        manager_mock.count.return_value = 1
        _Documento.investigacoes.em_curso.return_value = manager_mock
        orgao_id = '10'
        regras = [(30,), (50,)]
        _get_regras.return_value = regras

        url = reverse('dominio:suamesa-investigacoes', args=(orgao_id, ))
        resp = self.client.get(url)

        self.assertEqual(resp.data, {"suamesa_investigacoes": 1})
        self.assertEqual(resp.status_code, 200)
        _get_regras.assert_called_once_with(int(orgao_id), tipo='investigacao')
        _Documento.investigacoes.em_curso.assert_called_once_with(
            int(orgao_id), regras
        )
        manager_mock.count.assert_called_once_with()

    @mock.patch('dominio.views.suamesa.get_regras')
    @mock.patch('dominio.views.Documento')
    def test_sua_mesa_processos(self, _Documento, _get_regras):
        manager_mock = mock.MagicMock()
        manager_mock.count.return_value = 1
        _Documento.processos.em_juizo.return_value = manager_mock
        orgao_id = '10'
        regras = [(30,), (50,)]
        _get_regras.return_value = regras

        url = reverse('dominio:suamesa-processos', args=(orgao_id, ))
        resp = self.client.get(url)

        self.assertEqual(resp.data, {"suamesa_processos": 1})
        self.assertEqual(resp.status_code, 200)
        _get_regras.assert_called_once_with(int(orgao_id), tipo='processo')
        _Documento.processos.em_juizo.assert_called_once_with(
            int(orgao_id), regras
        )
        manager_mock.count.assert_called_once_with()

    @mock.patch('dominio.views.SubAndamento')
    def test_sua_mesa_finalizados(self, _SubAndamento):
        regras_saidas = (6251, 6657, 6655, 6644, 6326)
        manager_mock = mock.MagicMock()
        manager_mock.count.return_value = 1
        _SubAndamento.finalizados.trinta_dias.return_value = manager_mock
        orgao_id = '10'

        url = reverse('dominio:suamesa-finalizados', args=(orgao_id, ))
        resp = self.client.get(url)

        self.assertEqual(resp.data, {"suamesa_finalizados": 1})
        self.assertEqual(resp.status_code, 200)
        _SubAndamento.finalizados.trinta_dias.assert_called_once_with(
            int(orgao_id), regras_saidas
        )
        manager_mock.count.assert_called_once_with()

    @mock.patch('dominio.views.Vista')
    def test_sua_mesa_vistas_abertas(self, _Vista):
        manager_mock = mock.MagicMock()
        manager_mock.count.return_value = 1
        _Vista.vistas.abertas_promotor.return_value = manager_mock
        orgao_id = '10'
        cpf = '123456789'

        url = reverse('dominio:suamesa-vistas', args=(orgao_id, cpf))
        resp = self.client.get(url)

        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.data, {"suamesa_vistas": 1})
        _Vista.vistas.abertas_promotor.assert_called_once_with(
            int(orgao_id), cpf
        )
        manager_mock.count.assert_called_once_with()


class TestSuaMesaDetalheVistas(TestCase):
    @mock.patch('dominio.views.Vista')
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

    @mock.patch('dominio.views.Vista')
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


class TestSuaMesaListaVistasAbertas(TestCase):
    @mock.patch('dominio.views.Vista')
    def test_correct_response(self, _Vista):
        manager_mock = mock.MagicMock()
        filter_mock = mock.MagicMock()
        filter_mock.values.return_value = [
            {
                "numero_mprj": "1234",
                "numero_externo": "tj1234",
                "dt_abertura": date(2020, 1, 1),
                "classe": "classe 1",
            },
            {
                "numero_mprj": "9012",
                "numero_externo": "tj9012",
                "dt_abertura": date(2018, 1, 1),
                "classe": "classe 3",
            },
        ]
        manager_mock.filter.return_value = filter_mock

        _Vista.vistas.abertas_por_data.return_value = manager_mock

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

        resp = self.client.get(url)

        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.data, expected)

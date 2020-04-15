from unittest import mock

from django.conf import settings
from django.test import TestCase
from django.urls import reverse

from dominio.pip.views import PIPDetalheAproveitamentosView
from dominio.tests.testconf import NoJWTTestCase, NoCacheTestCase


class PIPDetalheAproveitamentosViewTest(
        NoJWTTestCase, NoCacheTestCase, TestCase):
    @mock.patch('dominio.pip.views.run_query')
    def test_get_numero_aproveitamentos_pips(self, _run_query):
        PIPDetalheAproveitamentosView\
            .get_numero_aproveitamentos_pips\
            .cache_clear()
        PIPDetalheAproveitamentosView\
            .get_numero_aproveitamentos_pips()

        expected_query = """
            SELECT
                orgao_id,
                nm_orgao,
                nr_aproveitamentos_periodo_atual,
                nr_aproveitamentos_periodo_anterior,
                variacao_periodo,
                tamanho_periodo_dias
            FROM {namespace}.tb_pip_detalhe_aproveitamentos
        """.format(namespace=settings.TABLE_NAMESPACE)

        _run_query.assert_called_once_with(expected_query)

    @mock.patch('dominio.pip.utils.run_query')
    @mock.patch('dominio.pip.views.run_query')
    def test_pip_aproveitamentos_result(self, _run_query, _run_query_aisps):
        _run_query.return_value = [
            (1, 'TC 1', 20, 50, 0.75),
            (2, 'TC 2', 30, 10, 0.5),
            (3, 'TC 3', 50, 40, 1.0),
            (4, 'TC 4', 10, 100, 0.75),
            (5, 'TC 5', 40, 30, 0.75)]
        _run_query_aisps.return_value = [
             (1, 1, 'AISP1'), (1, 2, 'AISP2'),
             (2, 1, 'AISP1'), (2, 2, 'AISP2'),
             (3, 3, 'AISP3'), (4, 3, 'AISP3'), (5, 3, 'AISP3')]

        PIPDetalheAproveitamentosView\
            .get_numero_aproveitamentos_pips\
            .cache_clear()
        response = self.client.get(reverse(
            'dominio:pip-aproveitamentos',
            args=('1')))

        expected_response = {
            'nr_aproveitamentos_30_dias': 20,
            'variacao_1_mes': 0.75,
            'top_n_pacote': [
                {'nm_promotoria': 'tc 3', 'nr_aproveitamentos_30_dias': 50},
                {'nm_promotoria': 'tc 5', 'nr_aproveitamentos_30_dias': 40},
                {'nm_promotoria': 'tc 2', 'nr_aproveitamentos_30_dias': 30}],
            'top_n_by_aisp': [
                {
                 'nr_aisp': 1,
                 'top_n': [
                     {'nm_promotoria': 'tc 2',
                      'nr_aproveitamentos_30_dias': 30},
                     {'nm_promotoria': 'tc 1',
                      'nr_aproveitamentos_30_dias': 20}]
                },
                {
                 'nr_aisp': 2,
                 'top_n': [
                     {'nm_promotoria': 'tc 2',
                      'nr_aproveitamentos_30_dias': 30},
                     {'nm_promotoria': 'tc 1',
                      'nr_aproveitamentos_30_dias': 20}]
                }
            ]
        }

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, expected_response)

    @mock.patch('dominio.pip.views.run_query')
    def test_pip_aproveitamentos_no_result(self, _run_query):
        _run_query.return_value = []
        PIPDetalheAproveitamentosView\
            .get_numero_aproveitamentos_pips\
            .cache_clear()
        response = self.client.get(reverse(
            'dominio:pip-aproveitamentos',
            args=('1')))

        expected_response = {'detail': 'Não encontrado.'}

        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.data, expected_response)


class PIPVistasAbertasMensalTest(NoJWTTestCase, NoCacheTestCase, TestCase):
    @mock.patch('dominio.pip.views.Vista')
    def test_pip_vistas_abertas_mensal(self, _Vista):
        manager_mock = mock.MagicMock()
        filter_mock = mock.MagicMock()
        values_mock = mock.MagicMock()
        distinct_mock = mock.MagicMock()

        manager_mock.count.return_value = 10

        manager_mock.filter.return_value = filter_mock
        filter_mock.values.return_value = values_mock
        values_mock.distinct.return_value = distinct_mock
        distinct_mock.count.return_value = 5

        _Vista.vistas.aberturas_30_dias_PIP.return_value = manager_mock
        orgao_id = '10'
        cpf = '123456789'

        url = reverse('dominio:pip-aberturas-mensal', args=(orgao_id, cpf))
        resp = self.client.get(url)

        expected_output = {
            'nr_aberturas_30_dias': 10,
            'nr_investigacoes_30_dias': 5
        }

        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.data, expected_output)
        _Vista.vistas.aberturas_30_dias_PIP.assert_called_once_with(
            int(orgao_id), cpf
        )
        manager_mock.count.assert_called_once_with()
        distinct_mock.count.assert_called_once_with()

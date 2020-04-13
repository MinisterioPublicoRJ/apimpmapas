from unittest import mock

from django.conf import settings
from django.test import TestCase
from django.urls import reverse

from dominio.pip_views import PIPDetalheAproveitamentosView
from .testconf import NoJWTTestCase, NoCacheTestCase


class PIPDetalheAproveitamentosViewTest(
        NoJWTTestCase, NoCacheTestCase, TestCase):
    @mock.patch('dominio.pip_views.run_query')
    def test_get_numero_aproveitamentos_pips(self, _run_query):
        PIPDetalheAproveitamentosView\
            .get_numero_aproveitamentos_pips()

        expected_query = """
            SELECT
                orgao_id,
                nm_orgao,
                nr_aproveitamentos_ultimos_30_dias,
                nr_aproveitamentos_ultimos_60_dias,
                variacao_1_mes
            FROM {namespace}.tb_pip_detalhe_aproveitamentos
        """.format(namespace=settings.TABLE_NAMESPACE)

        _run_query.assert_called_once_with(expected_query)

    @mock.patch('dominio.utils_pip.run_query')
    @mock.patch('dominio.pip_views.run_query')
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

    @mock.patch('dominio.pip_views.run_query')
    def test_pip_aproveitamentos_no_result(self, _run_query):
        _run_query.return_value = []
        response = self.client.get(reverse(
            'dominio:pip-aproveitamentos',
            args=('1')))

        expected_response = {'detail': 'Não encontrado.'}

        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.data, expected_response)
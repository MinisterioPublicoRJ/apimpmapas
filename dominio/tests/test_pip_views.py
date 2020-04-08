from datetime import datetime, timedelta
from unittest import mock

from django.conf import settings
from django.test import TestCase
from django.urls import reverse

from dominio.pip_views import PIPDetalheAproveitamentosView
from .testconf import NoJWTTestCase, NoCacheTestCase


class PIPDetalheAproveitamentosViewTest(NoJWTTestCase, NoCacheTestCase, TestCase):

    def test_get_value_from_orgao(self):
        test_orgao_id = 42
        test_list = [
            (1, 'Nome1', 220),
            (10, 'Nome2', 140),
            (42, 'Nome3', 150),
            (60, 'Nome4', 65)
        ]
        output = PIPDetalheAproveitamentosView.get_value_from_orgao(
            test_list, test_orgao_id, value_position=2)
        expected_output = 150

        self.assertEqual(output, expected_output)

    def test_get_value_from_invalid_orgao(self):
        test_orgao_id = 33
        test_list = [
            (1, 'Nome1', 220),
            (10, 'Nome2', 140),
            (42, 'Nome3', 150),
            (60, 'Nome4', 65)
        ]
        output = PIPDetalheAproveitamentosView.get_value_from_orgao(
            test_list, test_orgao_id, value_position=2)
        expected_output = None

        self.assertEqual(output, expected_output)

    def test_get_top_n_orgaos(self):
        test_list = [
            (1, 'Nome1', 220, 0.5, 10),
            (10, 'Nome2', 140, 0.3, 5),
            (42, 'Nome3', 150, -0.10, 20),
            (60, 'Nome4', 65, 1.0, 2)
        ]
        output = PIPDetalheAproveitamentosView.get_top_n_orgaos(
            test_list, orderby_position=4, n=3)
        expected_output = [
            {'nm_promotoria': 'Nome3', 'nr_aproveitamentos_30_dias': 20},
            {'nm_promotoria': 'Nome1', 'nr_aproveitamentos_30_dias': 10},
            {'nm_promotoria': 'Nome2', 'nr_aproveitamentos_30_dias': 5}
        ]

        self.assertEqual(output, expected_output)

    def test_get_orgaos_same_aisps(self):
        pass

    def test_get_top_n_by_aisp(self):
        pass

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

    @mock.patch('dominio.pip_views.run_query')
    def test_pip_aproveitamentos_result(self, _run_query):
        _run_query.side_effect = [
            [(1, 'TC 1', 20, 50, 0.75),
            (2, 'TC 2', 30, 10, 0.5),
            (3, 'TC 3', 50, 40, 1.0),
            (4, 'TC 4', 10, 100, 0.75),
            (5, 'TC 5', 40, 30, 0.75)],
            [(1, 1, 'AISP1'), (1, 2, 'AISP2'),
             (2, 1, 'AISP1'), (2, 2, 'AISP2'),
             (3, 3, 'AISP3'), (4, 3, 'AISP3'), (5, 3, 'AISP3'),]
        ]

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
                {'nr_aisp': 1,
                 'top_n': [
                     {'nm_promotoria': 'tc 2', 'nr_aproveitamentos_30_dias': 30},
                     {'nm_promotoria': 'tc 1', 'nr_aproveitamentos_30_dias': 20}]
                },
                {'nr_aisp': 2,
                 'top_n': [
                     {'nm_promotoria': 'tc 2', 'nr_aproveitamentos_30_dias': 30},
                     {'nm_promotoria': 'tc 1', 'nr_aproveitamentos_30_dias': 20}]
                }
            ]
        }

        print(response.data)
        print(expected_response)
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
from datetime import datetime, timedelta
from unittest import mock

from django.conf import settings
from django.test import TestCase
from django.urls import reverse

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
        output = DetalheProcessosJuizoView.get_value_from_orgao(
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
        output = DetalheProcessosJuizoView.get_value_from_orgao(
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
        output = DetalheProcessosJuizoView.get_top_n_orgaos(
            test_list, orderby_position=4, n=3)
        expected_output = [
            {'nm_promotoria': 'Nome3', 'nr_acoes_propostas_30_dias': 20},
            {'nm_promotoria': 'Nome1', 'nr_acoes_propostas_30_dias': 10},
            {'nm_promotoria': 'Nome2', 'nr_acoes_propostas_30_dias': 5}
        ]

        self.assertEqual(output, expected_output)

    def test_get_orgaos_same_aisps(self):
        self.assertEqual(1, 2)

    def test_get_top_n_by_aisp(self):
        self.assertEqual(1, 2)

    @mock.patch('dominio.views.run_query')
    def test_get_numero_aproveitamentos_pips(self, _run_query):
        DetalheProcessosJuizoView\
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

    @mock.patch('dominio.views.run_query')
    def test_pip_aproveitamentos_result(self, _run_query):
        _run_query.return_value = [
            (1, 'TC 1', 20, 1.0, 50),
            (2, 'TC 2', 30, 0.5, 10),
            (3, 'TC 3', 40, 0.75, 40),
            (4, 'TC 4', 10, 0.75, 100),
            (5, 'TC 5', 40, 0.75, 30)]

        response = self.client.get(reverse(
            'dominio:pip-aproveitamentos',
            args=('1')))

        expected_response = {
            'nr_acoes_propostas_60_dias': 20,
            'variacao_12_meses': 1.0,
            'top_n': [
                {'nm_promotoria': 'tc 4', 'nr_acoes_propostas_30_dias': 100},
                {'nm_promotoria': 'tc 1', 'nr_acoes_propostas_30_dias': 50},
                {'nm_promotoria': 'tc 3', 'nr_acoes_propostas_30_dias': 40}]
        }

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, expected_response)

    @mock.patch('dominio.views.run_query')
    def test_pip_aproveitamentos_no_result(self, _run_query):
        _run_query.return_value = []
        response = self.client.get(reverse(
            'dominio:pip-aproveitamentos',
            args=('1')))

        expected_response = {'detail': 'Não encontrado.'}

        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.data, expected_response)
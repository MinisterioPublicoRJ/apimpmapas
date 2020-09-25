from datetime import datetime
from decimal import Decimal
from unittest import mock

from django.conf import settings
from django.test import TestCase
from django.urls import reverse

from dominio.tutela.radar_views import RadarView
from dominio.tests.testconf import NoJWTTestCase, NoCacheTestCase


class TestSuaPromotoria(NoJWTTestCase, NoCacheTestCase, TestCase):
    @mock.patch("dominio.tutela.radar_views.run_query")
    def test_correct_response(self, _run_query):
        runquery_data = [
            (
                123,
                'Tutela Coletiva',
                Decimal('12345'),
                45,
                29,
                5,
                0,
                0,
                156,
                99,
                38,
                1,
                12,
                0.28846153846153844,
                0.29292929292929293,
                0.13157894736842105,
                0.0,
                0.0,
                53.5,
                47.0,
                20.0,
                0.0,
                1.5,
                -0.1588785046728972,
                -0.3829787234042553,
                -0.75,
                None,
                -1.0,
                datetime(2020, 3, 30, 10, 46, 14, 837000),
                'Promotoria de Justiça 1',
                'Promotoria de Justiça 2',
                'Promotoria de Justiça 3',
                '1ª Promotoria',
                '4ª Promotoria'
            )
        ]
        radar_query = """
            SELECT cod_pct,
            pacote_atribuicao,
            orgao_id,
            nr_arquivamentos,
            nr_indeferimentos,
            nr_instauracaoes,
            nr_tac,
            nr_acoes,
            max_pacote_arquivamentos,
            max_pacote_indeferimentos,
            max_pacote_instauracoes,
            max_pacote_tac,
            max_pacote_acoes,
            perc_arquivamentos,
            perc_indeferimentos,
            perc_instauracaoes,
            perc_tac,
            perc_acoes,
            med_pacote_arquivamentos,
            med_pacote_indeferimentos,
            med_pacote_instauracoes,
            med_pacote_tac,
            med_pacote_acoes,
            var_med_arquivaentos,
            var_med_indeferimentos,
            var_med_instauracoes,
            var_med_tac,
            var_med_acoes,
            dt_calculo,
            nm_max_arquivamentos,
            nm_max_indeferimentos,
            nm_max_instauracoes,
            nm_max_tac,
            nm_max_acoes
            FROM {schema}.tb_radar_performance
            WHERE orgao_id = :orgao_id
        """
        _run_query.return_value = runquery_data
        expected_data = runquery_data[0]

        url = reverse('dominio:radar', args=('1', ))
        expected_resp = dict(zip(RadarView.field_names, expected_data))

        resp = self.client.get(url)

        self.assertEqual(resp.status_code, 200)
        _run_query.assert_called_with(
            radar_query.format(schema=settings.TABLE_NAMESPACE),
            parameters={"orgao_id": 1}
        )
        self.assertEqual(resp.data, expected_resp)

    @mock.patch("dominio.tutela.radar_views.run_query")
    def test_404_response(self, _run_query):
        _run_query.return_value = None

        url = reverse('dominio:radar', args=('nonexist', ))

        resp = self.client.get(url)

        self.assertEqual(resp.status_code, 404)

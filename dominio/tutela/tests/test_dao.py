from datetime import datetime

from django.test import TestCase

from dominio.tests.testconf import NoCacheTestCase
from dominio.tutela.dao import RadarPerformanceDAO


class TestRadarPerformanceDAO(NoCacheTestCase, TestCase):
    def test_serialize_result(self):
        result_set = [
            (
                16,
                "Tutela de Tal Coisa",
                29933850,
                3,
                2,
                0,
                0,
                12,
                15,
                6,
                0,
                6,
                486,
                0.42857142857142855,
                0.3333333333333333,
                None,
                0.0,
                0.030864197530864196,
                3.0,
                5.0,
                0.0,
                0.0,
                79.0,
                0.0,
                -0.6,
                None,
                None,
                -0.810126582278481,
                datetime(2020, 4, 22, 13, 36, 6, 668000),
                "1ª PROMOTORIA DE JUSTIÇA",
                "2ª PROMOTORIA DE JUSTIÇA",
                "3ª PROMOTORIA DE JUSTIÇA",
                "4ª PROMOTORIA DE JUSTIÇa",
                "5ª PROMOTORIA DE JUSTIÇA",
            ),
        ]
        ser_data = RadarPerformanceDAO.serialize(result_set)
        expected_data = {
            "cod_pct": 16,
            "pacote_atribuicao": "Tutela de Tal Coisa",
            "orgao_id": 29933850,
            "nr_arquivamentos": 3,
            "nr_indeferimentos": 2,
            "nr_instauracoes": 0,
            "nr_tac": 0,
            "nr_acoes": 12,
            "max_pacote_arquivamentos": 15,
            "max_pacote_indeferimentos": 6,
            "max_pacote_instauracoes": 0,
            "max_pacote_tac": 6,
            "max_pacote_acoes": 486,
            "perc_arquivamentos": 0.42857142857142855,
            "perc_indeferimentos": 0.3333333333333333,
            "perc_instauracoes": None,
            "perc_tac": 0.0,
            "perc_acoes": 0.030864197530864196,
            "med_pacote_aquivamentos": 3.0,
            "med_pacote_indeferimentos": 5.0,
            "med_pacote_instauracoes": 0.0,
            "med_pacote_tac": 0.0,
            "med_pacote_acoes": 79.0,
            "var_med_arquivamentos": 0.0,
            "var_med_indeferimentos": -0.6,
            "var_med_instauracoes": None,
            "var_med_tac": None,
            "var_med_acoes": -0.810126582278481,
            "dt_calculo": '2020-04-22T13:36:06.668000Z',
            "nm_max_arquivamentos": "1ª Promotoria de Justiça",
            "nm_max_indeferimentos": "2ª Promotoria de Justiça",
            "nm_max_instauracoes": "3ª Promotoria de Justiça",
            "nm_max_tac": "4ª Promotoria de Justiça",
            "nm_max_acoes": "5ª Promotoria de Justiça",
        }
        assert ser_data == expected_data
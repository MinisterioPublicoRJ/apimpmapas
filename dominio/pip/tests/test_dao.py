from datetime import datetime
from unittest import mock

import pytest

from dominio.exceptions import APIEmptyResultError
from dominio.pip.dao import PIPRadarPerformanceDAO, QUERIES_DIR


class TestPIPRadarPerformance:
    @mock.patch("dominio.pip.dao.impala_execute")
    def test_execute_query(self, _impalaa_execute):
        with open(QUERIES_DIR.child("pip_radar_performance.sql")) as fobj:
            query = fobj.read()

        orgao_id = "12345"
        PIPRadarPerformanceDAO.execute(orgao_id=orgao_id)

        _impalaa_execute.assert_called_once_with(
            query, {"orgao_id": orgao_id}
        )

    def test_serialize_result(self):
        result_set = [(
            16,
            '16',
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
            '1ª PROMOTORIA DE JUSTIÇA',
            '2ª PROMOTORIA DE JUSTIÇA',
            '3ª PROMOTORIA DE JUSTIÇA',
            '4ª PROMOTORIA DE JUSTIÇa',
            '5ª PROMOTORIA DE JUSTIÇA',
        ), ]
        ser_data = PIPRadarPerformanceDAO.serialize(result_set)
        expected_data = {
            "aisp_codigo": 16,
            "aisp_nome": '16',
            "orgao_id": 29933850,
            "nr_denuncias": 3,
            "nr_cautelares": 2,
            "nr_acordos_n_persecucao": 0,
            "nr_arquivamentos": 0,
            "nr_aberturas_vista": 12,
            "max_aisp_denuncias": 15,
            "max_aisp_cautelares": 6,
            "max_aisp_acordos": 0,
            "max_aisp_arquivamentos": 6,
            "max_aisp_aberturas_vista": 486,
            "perc_denuncias": 0.42857142857142855,
            "perc_cautelares": 0.3333333333333333,
            "perc_acordos": None,
            "perc_arquivamentos": 0.0,
            "perc_aberturas_vista": 0.030864197530864196,
            "med_aisp_denuncias": 3.0,
            "med_aisp_cautelares": 5.0,
            "med_aisp_acordos": 0.0,
            "med_aisp_arquivamentos": 0.0,
            "med_aisp_aberturas_vista": 79.0,
            "var_med_denuncias": 0.0,
            "var_med_cautelares": -0.6,
            "var_med_acordos": None,
            "var_med_arquivamentos": None,
            "var_med_aberturas_vista": -0.810126582278481,
            "dt_calculo": datetime(2020, 4, 22, 13, 36, 6, 668000),
            "nm_max_denuncias": "1ª Promotoria de Justiça",
            "nm_max_cautelares": "2ª Promotoria de Justiça",
            "nm_max_acordos": "3ª Promotoria de Justiça",
            "nm_max_arquivamentos": "4ª Promotoria de Justiça",
            "nm_max_abeturas_vista": "5ª Promotoria de Justiça",
        }
        assert ser_data == expected_data

    @mock.patch.object(PIPRadarPerformanceDAO, "execute")
    @mock.patch.object(PIPRadarPerformanceDAO, "serialize")
    def test_get_data(self, _serialize, _execute):
        result_set = [(0.133)]
        _execute.return_value = result_set
        _serialize.return_value = {"data": 1}

        orgao_id = "12345"
        data = PIPRadarPerformanceDAO.get(orgao_id=orgao_id)

        _execute.assert_called_once_with(orgao_id=orgao_id)
        _serialize.assert_called_once_with(result_set)
        assert data == {"data": 1}

    @mock.patch.object(PIPRadarPerformanceDAO, "execute")
    @mock.patch.object(PIPRadarPerformanceDAO, "serialize")
    def test_get_data_404_exception(self, _serialize, _execute):
        result_set = []
        _execute.return_value = result_set

        orgao_id = "12345"
        with pytest.raises(APIEmptyResultError):
            PIPRadarPerformanceDAO.get(orgao_id=orgao_id)

        _execute.assert_called_once_with(orgao_id=orgao_id)
        _serialize.assert_not_called()

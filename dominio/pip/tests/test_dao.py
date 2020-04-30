from datetime import datetime
from unittest import mock

import pytest
from django.conf import settings
from rest_framework import serializers

from dominio.exceptions import APIEmptyResultError
from dominio.pip.dao import (
    GenericDAO,
    PIPRadarPerformanceDAO,
    PIPPrincipaisInvestigadosDAO,
    QUERIES_DIR,
)


class TestGenericDAO:
    @mock.patch('dominio.pip.dao.GenericDAO.table_namespaces',
                new_callable=mock.PropertyMock)
    @mock.patch('dominio.pip.dao.GenericDAO.query_file',
                new_callable=mock.PropertyMock)
    def test_query_method(self, _query_file, _namespaces):
        _query_file.return_value = "test_query.sql"
        _namespaces.return_value = {"schema": "test_schema"}

        with open(QUERIES_DIR.child("test_query.sql")) as fobj:
            query = fobj.read()
        expected_query = query.format(schema="test_schema")

        output = GenericDAO.query()

        assert output == expected_query

    @mock.patch.object(GenericDAO, "query")
    @mock.patch("dominio.pip.dao.impala_execute")
    def test_execute_method(self, _impala_execute, _query):
        _query.return_value = "SELECT * FROM dual"

        orgao_id = "12345"
        GenericDAO.execute(orgao_id=orgao_id)

        _impala_execute.assert_called_once_with(
            "SELECT * FROM dual", {"orgao_id": orgao_id}
        )

    @mock.patch('dominio.pip.dao.GenericDAO.columns',
                new_callable=mock.PropertyMock)
    def test_serialize_result_no_serializer(self, _columns):
        _columns.return_value = ["col1", "col2", "col3"]
        result_set = [
            ("1", "2", "3"),
            ("4", "5", "6"),
            ("7", "8", "9"),
        ]
        ser_data = GenericDAO.serialize(result_set)
        expected_data = [
            {"col1": "1", "col2": "2", "col3": "3"},
            {"col1": "4", "col2": "5", "col3": "6"},
            {"col1": "7", "col2": "8", "col3": "9"},
        ]
        assert ser_data == expected_data

    @mock.patch('dominio.pip.dao.GenericDAO.serializer',
                new_callable=mock.PropertyMock)
    @mock.patch('dominio.pip.dao.GenericDAO.columns',
                new_callable=mock.PropertyMock)
    def test_serialize_result_with_serializer(self, _columns, _serializer):
        class TestSerializer(serializers.Serializer):
            col1 = serializers.IntegerField()
            col2 = serializers.IntegerField()
            col3 = serializers.IntegerField()

        _serializer.return_value = TestSerializer
        _columns.return_value = ["col1", "col2", "col3"]
        result_set = [
            ("1", "2", "3"),
            ("4", "5", "6"),
            ("7", "8", "9"),
        ]
        ser_data = GenericDAO.serialize(result_set)
        expected_data = [
            {"col1": 1, "col2": 2, "col3": 3},
            {"col1": 4, "col2": 5, "col3": 6},
            {"col1": 7, "col2": 8, "col3": 9},
        ]

        assert ser_data == expected_data

    @mock.patch.object(GenericDAO, "execute")
    @mock.patch.object(GenericDAO, "serialize")
    def test_get_data(self, _serialize, _execute):
        result_set = [("0.133")]
        _execute.return_value = result_set
        _serialize.return_value = {"data": 1}

        orgao_id = "12345"
        data = GenericDAO.get(orgao_id=orgao_id)

        _execute.assert_called_once_with(orgao_id=orgao_id)
        _serialize.assert_called_once_with(result_set)
        assert data == {"data": 1}

    @mock.patch.object(GenericDAO, "execute")
    @mock.patch.object(GenericDAO, "serialize")
    def test_get_data_404_exception(self, _serialize, _execute):
        result_set = []
        _execute.return_value = result_set

        orgao_id = "12345"
        with pytest.raises(APIEmptyResultError):
            GenericDAO.get(orgao_id=orgao_id)

        _execute.assert_called_once_with(orgao_id=orgao_id)
        _serialize.assert_not_called()


class TestPIPRadarPerformance:
    def test_query_method(self):
        with open(QUERIES_DIR.child("pip_radar_performance.sql")) as fobj:
            query = fobj.read()

        cls = PIPRadarPerformanceDAO
        expected_query = query.format(schema=settings.TABLE_NAMESPACE)

        assert cls.query() == expected_query

    def test_serialize_result(self):
        result_set = [
            (
                16,
                "16",
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
        ser_data = PIPRadarPerformanceDAO.serialize(result_set)
        expected_data = {
            "aisp_codigo": 16,
            "aisp_nome": "16",
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


class TestPIPPrincipaisInvestigadosDAO:
    @mock.patch("dominio.pip.dao.get_hbase_table")
    def test_get_hbase_flags(self, _get_table):
        table_mock = mock.MagicMock()
        table_mock.scan.return_value = [
            (
                b"1",
                {
                    b"identificacao:nm_personagem": b"Nome1",
                    b"flags:is_pinned": b"True",
                    b"flags:is_removed": b"False"
                }
            ),
            (
                b"2",
                {
                    b"identificacao:nm_personagem": b"Nome2",
                    b"flags:is_pinned": b"True"
                }
            )
        ]
        _get_table.return_value = table_mock

        expected_output = {
            "Nome1": {"is_pinned": True, "is_removed": False},
            "Nome2": {"is_pinned": True, "is_removed": False},
        }

        data = PIPPrincipaisInvestigadosDAO.get_hbase_flags("1", "2")

        hbspace = settings.HBASE_NAMESPACE
        _get_table.assert_called_once_with(hbspace + "pip_investigados_flags")
        table_mock.scan.assert_called_once_with(row_prefix=b"12")
        assert data == expected_output

    @mock.patch("dominio.pip.dao.get_hbase_table")
    def test_save_hbase_flags(self, _get_table):
        table_mock = mock.MagicMock()
        table_mock.put.return_value = None
        _get_table.return_value = table_mock

        expected_output = {
            "identificacao:orgao_id": "1",
            "identificacao:cpf": "2",
            "identificacao:nm_personagem": "Nome1",
            "flags:is_pinned": "True",
            "flags:is_removed": "False"
        }

        expected_call_arguments = {
            b"identificacao:orgao_id": b"1",
            b"identificacao:cpf": b"2",
            b"identificacao:nm_personagem": b"Nome1",
            b"flags:is_pinned": b"True",
            b"flags:is_removed": b"False"
        }

        data = PIPPrincipaisInvestigadosDAO.save_hbase_flags(
            "1", "2", "Nome1", "True", "False")

        hbspace = settings.HBASE_NAMESPACE
        _get_table.assert_called_once_with(hbspace + "pip_investigados_flags")
        table_mock.put.assert_called_once_with(
            b"12Nome1", expected_call_arguments)
        assert expected_output == data

    @mock.patch.object(PIPPrincipaisInvestigadosDAO, "get_hbase_flags")
    @mock.patch.object(GenericDAO, "get")
    def test_get(self, _get, _get_hbase):
        _get_hbase.return_value = {
            'Nome2': {'is_pinned': True, 'is_removed': False},
            'Nome3': {'is_pinned': False, 'is_removed': True},
        }
        _get.return_value = [
            {
                'nm_investigado': 'Nome1',
                'pip_codigo': 1,
                'nr_investigacoes': 10
            },
            {
                'nm_investigado': 'Nome2',
                'pip_codigo': 1,
                'nr_investigacoes': 5
            },
            {
                'nm_investigado': 'Nome3',
                'pip_codigo': 1,
                'nr_investigacoes': 15
            },
        ]

        expected_output = [
            {
                'nm_investigado': 'Nome2',
                'pip_codigo': 1,
                'nr_investigacoes': 5,
                'is_pinned': True,
                'is_removed': False
            },
            {
                'nm_investigado': 'Nome1',
                'pip_codigo': 1,
                'nr_investigacoes': 10,
                'is_pinned': False,
                'is_removed': False
            },
        ]

        data = PIPPrincipaisInvestigadosDAO.get("1", "2")
        assert data == expected_output

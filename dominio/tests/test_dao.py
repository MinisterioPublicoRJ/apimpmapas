from unittest import mock

import pytest
from rest_framework import serializers
from django.conf import settings

from dominio.exceptions import APIEmptyResultError
from dominio.dao import (
    GenericDAO
)

QUERIES_DIR = settings.BASE_DIR.child("dominio", "tests", "queries")


class TestGenericDAO:
    @mock.patch("dominio.dao.GenericDAO.QUERIES_DIR",
                new_callable=mock.PropertyMock)
    @mock.patch("dominio.dao.GenericDAO.table_namespaces",
                new_callable=mock.PropertyMock)
    @mock.patch("dominio.dao.GenericDAO.query_file",
                new_callable=mock.PropertyMock)
    def test_query_method(self, _query_file, _namespaces, _queries_dir):
        _query_file.return_value = "test_query.sql"
        _namespaces.return_value = {"schema": "test_schema"}
        _queries_dir.return_value = QUERIES_DIR

        with open(QUERIES_DIR.child("test_query.sql")) as fobj:
            query = fobj.read()
        expected_query = query.format(schema="test_schema")

        output = GenericDAO.query()

        assert output == expected_query

    @mock.patch.object(GenericDAO, "query")
    @mock.patch("dominio.dao.impala_execute")
    def test_execute_method(self, _impala_execute, _query):
        _query.return_value = "SELECT * FROM dual"

        orgao_id = "12345"
        GenericDAO.execute(orgao_id=orgao_id)

        _impala_execute.assert_called_once_with(
            "SELECT * FROM dual", {"orgao_id": orgao_id}
        )

    @mock.patch("dominio.dao.GenericDAO.columns",
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

    @mock.patch("dominio.dao.GenericDAO.serializer",
                new_callable=mock.PropertyMock)
    @mock.patch("dominio.dao.GenericDAO.columns",
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

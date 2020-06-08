from unittest import mock

from django.test import TestCase


from mprj_api.db_routers import DominioRouter
from dominio.db_connectors import (
    BDA_Error,
    execute,
    run_query,
    get_hbase_table,
)
from lupa.exceptions import QueryError


class DominioDbTest(TestCase):

    def test_db_router(self):
        router = DominioRouter()
        model = mock.MagicMock()
        model._meta.app_label = 'dominio'

        result = router.db_for_read(model)
        self.assertEqual(result, 'dominio_db')

    @mock.patch('dominio.db_connectors.bda_connect')
    def test_impala_query(self, _bda_connect):
        query = 'MOCK QUERY'

        cursor = mock.MagicMock()
        _bda_connect.return_value.__enter__\
            .return_value.cursor.return_value.__enter__\
            .return_value = cursor
        execute(query, None)

        cursor.execute.assert_called_once_with(query, None)

    @mock.patch('dominio.db_connectors.bda_connect')
    def test_impala_query_fail(self, _bda_connect):
        query = 'MOCK QUERY'

        cursor = mock.MagicMock()
        cursor.execute.side_effect = BDA_Error('test error')

        with self.assertRaises(QueryError):
            _bda_connect.return_value.__enter__\
                .return_value.cursor.return_value.__enter__\
                .return_value = cursor
            execute(query, None)

        cursor.execute.assert_called_once_with(query, None)

    def test_query_error(self):
        pass


class RunQuery(TestCase):
    @mock.patch(
        "dominio.db_connectors.execute", return_value=[("result set", )]
    )
    def test_run_query(self, _execute):
        query = "SELECT * FROM dual()"
        resp = run_query(query)

        _execute.assert_called_once_with(query, None)
        self.assertEqual(resp, [("result set",)])

    @mock.patch("dominio.db_connectors.execute")
    def test_run_query_error(self, _execute):
        _execute.side_effect = QueryError
        query = "SELECT * FROM dual()"
        resp = run_query(query)

        _execute.assert_called_once_with(query, None)
        self.assertEqual(resp, None)

    @mock.patch("dominio.db_connectors.execute", return_value=[])
    def test_run_query_empty_response(self, _execute):
        query = "SELECT * FROM dual()"
        resp = run_query(query)

        _execute.assert_called_once_with(query, None)
        self.assertEqual(resp, None)


class HBaseTests(TestCase):
    @mock.patch("dominio.db_connectors.HBaseConnection")
    def test_hbase_get_table(self, _HBaseConnection):
        connection_mock = mock.MagicMock()
        connection_mock.table.return_value = "Table"
        _HBaseConnection.return_value = connection_mock

        output = get_hbase_table("tabela")

        self.assertEqual(output, "Table")
        connection_mock.table.assert_called_once_with("tabela")

    @mock.patch("dominio.db_connectors.HBaseConnection")
    def test_hbase_get_table_failed_connection(self, _HBaseConnection):
        _HBaseConnection.side_effect = Exception

        with self.assertRaises(Exception):
            get_hbase_table("tabela")

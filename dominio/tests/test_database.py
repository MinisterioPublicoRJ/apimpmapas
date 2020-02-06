from unittest import mock

from django.test import TestCase


from mprj_api.db_routers import DominioRouter
from dominio.db_connectors import BDA_Error, execute
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
        execute(query)

        cursor.execute.assert_called_once_with(query)

    @mock.patch('dominio.db_connectors.bda_connect')
    def test_impala_query_fail(self, _bda_connect):
        query = 'MOCK QUERY'

        cursor = mock.MagicMock()
        cursor.execute.side_effect = BDA_Error('test error')

        with self.assertRaises(QueryError):
            _bda_connect.return_value.__enter__\
                .return_value.cursor.return_value.__enter__\
                .return_value = cursor
            execute(query)

        cursor.execute.assert_called_once_with(query)

from unittest import TestCase, mock

from decouple import config

from api.db_connectors import postgres_access


class Database_access(TestCase):
    @mock.patch('api.db_connectors.postgres_connect')
    def test_connect_postgres(self, _postgres_connect):
        query = 'SELECT * FROM TABELA'

        cursor = mock.MagicMock()
        _postgres_connect.return_value.__enter__\
            .return_value.cursor.return_value.__enter__\
            .return_value = cursor

        postgres_access(query)

        _postgres_connect.assert_called_once_with(
            host=config('PG_HOST'),
            dbname=config('PG_BASE'),
            user=config('PG_USER')
        )
        cursor.execute.assert_called_once_with(query)

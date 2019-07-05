from unittest import TestCase, mock

from decouple import config

from api.db_connectors import postgres_access, generate_query


class Database_access(TestCase):
    @mock.patch('api.db_connectors.pg_connect')
    def test_connect_postgres(self, _pg_connect):
        query = 'SELECT "col1", "col2" FROM "schema"."tabela" WHERE "col_id" = 00'

        cursor = mock.MagicMock()
        _pg_connect.return_value.__enter__\
            .return_value.cursor.return_value.__enter__\
            .return_value = cursor

        postgres_access(query, domain_id='00')

        _pg_connect.assert_called_once_with(
            host=config('PG_HOST'),
            dbname=config('PG_BASE'),
            user=config('PG_USER')
        )
        cursor.execute.assert_called_once_with(query)

    def test_generate_query(self):
        expected_query = "SELECT col1, col2 FROM schema.tabela"\
                         " WHERE col_id = %s"

        db = 'PG'
        schema = 'schema'
        table = 'tabela'
        columns = ['col1', 'col2']
        id_column = 'col_id'

        query = generate_query(
            db,
            schema,
            table,
            columns,
            id_column
        )

        self.assertEqual(query, expected_query)
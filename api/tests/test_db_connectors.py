from unittest import TestCase, mock

from decouple import config

from api.db_connectors import postgres_access, generate_query


class Database_access(TestCase):
    def setUp(self):
        self.query = 'SELECT col1, col2 FROM schema.tabela WHERE '\
                              'col_id = %s'
        self.db = 'PG'
        self.schema = 'schema'
        self.table = 'tabela'
        self.columns = ['col1', 'col2']
        self.id_column = 'col_id'
        self.domain_id = '00'

    @mock.patch('api.db_connectors.pg_connect')
    def test_connect_postgres(self, _pg_connect):

        cursor = mock.MagicMock()
        _pg_connect.return_value.__enter__\
            .return_value.cursor.return_value.__enter__\
            .return_value = cursor

        postgres_access(self.query, self.domain_id)

        _pg_connect.assert_called_once_with(
            host=config('PG_HOST'),
            dbname=config('PG_BASE'),
            user=config('PG_USER')
        )
        cursor.execute.assert_called_once_with(self.query, (self.domain_id,))

    def test_generate_query(self):
        gen_query = generate_query(
            self.db,
            self.schema,
            self.table,
            self.columns,
            self.id_column
        )

        self.assertEqual(gen_query, self.query)

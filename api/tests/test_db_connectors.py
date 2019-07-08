from unittest import TestCase, mock

from decouple import config

from api.db_connectors import (
    oracle_access,
    postgres_access,
    generate_query
)


class CommonSetup(TestCase):

    def setUp(self):
        self.query = 'SELECT col1, col2 FROM schema.tabela WHERE '\
                              'col_id = %s'
        self.schema = 'schema'
        self.table = 'tabela'
        self.columns = ['col1', 'col2']
        self.id_column = 'col_id'
        self.domain_id = '00'


class CommonsTestCase(CommonSetup):

    def test_generate_query(self):
        gen_query = generate_query(
            self.schema,
            self.table,
            self.columns,
            self.id_column
        )

        self.assertEqual(gen_query, self.query)


class PostgresAccess(CommonSetup):

    def setUp(self):
        super().setUp()
        self.db = 'PG'

    @mock.patch('api.db_connectors.pg_connect')
    def test_connect_postgres(self, _pg_connect):

        postgres_access(self.query, self.domain_id)

        _pg_connect.assert_called_once_with(
            host=config('PG_HOST'),
            dbname=config('PG_BASE'),
            user=config('PG_USER')
        )

    @mock.patch('api.db_connectors.pg_connect')
    def test_execute_postgres(self, _pg_connect):

        cursor = mock.MagicMock()
        _pg_connect.return_value.__enter__\
            .return_value.cursor.return_value.__enter__\
            .return_value = cursor

        postgres_access(self.query, self.domain_id)

        cursor.execute.assert_called_once_with(self.query, (self.domain_id,))
        cursor.fetchall.assert_called_once_with()


class OracleAccess(CommonSetup):

    def setUp(self):
        super().setUp()
        self.db = 'ORA'

    @mock.patch('api.db_connectors.ora_connect')
    def test_connect_oracle(self, _ora_connect):
        oracle_access(self.query, self.domain_id)

        _ora_connect.assert_called_once_with(
            user=config('ORA_USER'),
            password=config('ORA_PASS'),
            dsn=config('ORA_HOST')
        )

    @mock.patch('api.db_connectors.ora_connect')
    def test_execute_oracle(self, _ora_connect):
        cursor = mock.MagicMock()
        _ora_connect.return_value.__enter__\
            .return_value.cursor.return_value.__enter__\
            .return_value = cursor

        oracle_access(self.query, self.domain_id)

        cursor.execute.assert_called_once_with(self.query, (self.domain_id,))
        cursor.fetchall.assert_called_once_with()

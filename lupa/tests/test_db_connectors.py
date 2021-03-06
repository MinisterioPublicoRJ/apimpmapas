from unittest import TestCase, mock

from django.conf import settings

from lupa.db_connectors import (
    bda_access,
    execute as db_execute,
    execute_sample,
    execute_geospatial,
    oracle_access,
    postgres_access,
    generate_query,
    generate_query_sample,
    generate_geospatial_query,
    BDA_Error,
    ORA_Error,
    PG_Error,
    QueryError,
)


class CommonSetup(TestCase):

    def setUp(self):
        self.schema = 'schema'
        self.table = 'tabela'
        self.columns = ['col1', 'col2']
        self.id_column = 'col_id'
        self.domain_id = '00'


class PostgresAccess(CommonSetup):

    def setUp(self):
        super().setUp()
        self.query = 'SELECT col1, col2 FROM schema.tabela WHERE '\
                     'col_id = %s'
        self.db = 'PG'

    @mock.patch('lupa.db_connectors.pg_connect')
    def test_connect_postgres(self, _pg_connect):

        postgres_access(self.query, self.domain_id)

        _pg_connect.assert_called_once_with(
            host=settings.PG_HOST,
            dbname=settings.PG_BASE,
            user=settings.PG_USER,
            password=settings.PG_PASSWORD
        )

    def test_generate_query_postgres(self):
        gen_query = generate_query(
            self.db,
            self.schema,
            self.table,
            self.columns,
            self.id_column
        )

        self.assertEqual(gen_query, self.query)

    @mock.patch(
        'lupa.db_connectors.generate_query',
        return_value='generated_query'
    )
    @mock.patch('lupa.db_connectors.postgres_access')
    def test_call_correct_pg(self, _postgres_access, _generate_query):
        db_execute(
            self.db,
            self.schema,
            self.table,
            self.columns,
            self.id_column,
            self.domain_id
        )

        _generate_query.assert_called_once_with(
            self.db,
            self.schema,
            self.table,
            self.columns,
            self.id_column
        )
        _postgres_access.assert_called_once_with(
            'generated_query',
            (self.domain_id,)
        )

    @mock.patch('lupa.db_connectors.pg_connect')
    def test_execute_postgres(self, _pg_connect):

        cursor = mock.MagicMock()
        _pg_connect.return_value.__enter__\
            .return_value.cursor.return_value.__enter__\
            .return_value = cursor

        postgres_access(self.query, (self.domain_id,))

        cursor.execute.assert_called_once_with(self.query, (self.domain_id,))
        cursor.fetchall.assert_called_once_with()

    @mock.patch('lupa.db_connectors.pg_connect')
    def test_query_wrong_postgres(self, _pg_connect):
        cursor = mock.MagicMock()
        cursor.execute.side_effect = PG_Error('test error')

        with self.assertRaises(QueryError):
            _pg_connect.return_value.__enter__\
                .return_value.cursor.return_value.__enter__\
                .return_value = cursor

            postgres_access(self.query, self.domain_id)


class OracleAccess(CommonSetup):

    def setUp(self):
        super().setUp()
        self.db = 'ORA'
        self.query = 'SELECT col1, col2 FROM schema.tabela WHERE '\
                     'col_id = :1'

    @mock.patch('lupa.db_connectors.ora_connect')
    def test_connect_oracle(self, _ora_connect):
        oracle_access(self.query, self.domain_id)

        _ora_connect.assert_called_once_with(
            user=settings.ORA_USER,
            password=settings.ORA_PASS,
            dsn=settings.ORA_HOST
        )

    def test_generate_query_oracle(self):
        gen_query = generate_query(
            self.db,
            self.schema,
            self.table,
            self.columns,
            self.id_column
        )

        self.assertEqual(gen_query, self.query)

    @mock.patch(
        'lupa.db_connectors.generate_query',
        return_value='generated_query'
    )
    @mock.patch('lupa.db_connectors.oracle_access')
    def test_call_correct_ora(self, _oracle_access, _generate_query):
        db_execute(
            self.db,
            self.schema,
            self.table,
            self.columns,
            self.id_column,
            self.domain_id
        )

        _generate_query.assert_called_once_with(
            self.db,
            self.schema,
            self.table,
            self.columns,
            self.id_column
        )
        _oracle_access.assert_called_once_with(
            'generated_query',
            (self.domain_id,)
        )

    @mock.patch('lupa.db_connectors.ora_connect')
    def test_execute_oracle(self, _ora_connect):
        cursor = mock.MagicMock()
        _ora_connect.return_value.__enter__\
            .return_value.cursor.return_value.__enter__\
            .return_value = cursor

        oracle_access(self.query, (self.domain_id,))

        cursor.execute.assert_called_once_with(self.query, (self.domain_id,))
        cursor.fetchall.assert_called_once_with()

    @mock.patch('lupa.db_connectors.ora_connect')
    def test_query_wrong_oracle(self, _ora_connect):
        cursor = mock.MagicMock()
        cursor.execute.side_effect = ORA_Error('test error')

        with self.assertRaises(QueryError):
            _ora_connect.return_value.__enter__\
                .return_value.cursor.return_value.__enter__\
                .return_value = cursor

            oracle_access(self.query, self.domain_id)


class BdaAccess(CommonSetup):

    def setUp(self):
        super().setUp()
        self.db = 'BDA'
        self.query = 'SELECT col1, col2 FROM schema.tabela WHERE '\
                     'col_id = :1'

    @mock.patch('lupa.db_connectors.bda_connect')
    def test_connect_dba(self, _bda_connect):
        bda_access(self.query, (self.domain_id,))

        _bda_connect.assert_called_once_with(
            host=settings.IMPALA_HOST,
            port=settings.IMPALA_PORT,
            use_ssl=False,
            user=settings.KERBEROS_USER,
            kerberos_service_name=settings.KERBEROS_SERVICE_NAME,
            auth_mechanism='GSSAPI'
        )

    def test_generate_query_bda(self):
        gen_query = generate_query(
            self.db,
            self.schema,
            self.table,
            self.columns,
            self.id_column
        )

        self.assertEqual(gen_query, self.query)

    @mock.patch(
        'lupa.db_connectors.generate_query',
        return_value='generated_query'
    )
    @mock.patch('lupa.db_connectors.bda_access')
    def test_call_correct_pg(self, _bda_access, _generate_query):
        db_execute(
            self.db,
            self.schema,
            self.table,
            self.columns,
            self.id_column,
            self.domain_id
        )

        _generate_query.assert_called_once_with(
            self.db,
            self.schema,
            self.table,
            self.columns,
            self.id_column
        )
        _bda_access.assert_called_once_with(
            'generated_query',
            (self.domain_id,)
        )

    @mock.patch('lupa.db_connectors.bda_connect')
    def test_execute_dba(self, _bda_connect):
        cursor = mock.MagicMock()
        _bda_connect.return_value.__enter__\
            .return_value.cursor.return_value.__enter__\
            .return_value = cursor

        bda_access(self.query, (self.domain_id, ))

        cursor.execute.assert_called_once_with(self.query, (self.domain_id,))
        cursor.fetchall.assert_called_once_with()

    @mock.patch('lupa.db_connectors.bda_connect')
    def test_query_wrong_bda(self, _bda_connect):
        cursor = mock.MagicMock()
        cursor.execute.side_effect = BDA_Error('test error')

        with self.assertRaises(QueryError):
            _bda_connect.return_value.__enter__\
                .return_value.cursor.return_value.__enter__\
                .return_value = cursor

            bda_access(self.query, self.domain_id)


class Geospatial(CommonSetup):
    def test_geospatial_build_query(self):
        expected_qeuery = (
            'select col_id\n'
            '               from schema.tabela\n'
            '               where ST_Contains(\n'
            '                    st_geomfromgeojson(geo_json),\n'
            "                    st_geomfromtext('POINT(-22.4 -43.2)')\n"
            '               )')

        query = generate_geospatial_query(
            self.schema,
            self.table,
            "geo_json",
            self.id_column,
            [-43.2, -22.4]
        )

        self.assertSequenceEqual(query, expected_qeuery)

    def test_avoid_geospatial_injection(self):
        with self.assertRaises(ValueError):
            generate_geospatial_query(
                self.schema,
                self.table,
                "geo_json",
                self.id_column,
                ['(;-43.2', -22.4]
            )

    def test_geospatial_wrong_database(self):
        with self.assertRaises(NotImplementedError):
            execute_geospatial(
                'ORA',
                self.schema,
                self.table,
                'geojson',
                self.id_column,
                []
            )

    @mock.patch(
        'lupa.db_connectors.generate_geospatial_query',
        return_value="generated_query")
    @mock.patch('lupa.db_connectors.postgres_access')
    def test_call_correct_database(self, _pga, _ggq):
        execute_geospatial(
            'PG',
            self.schema,
            self.table,
            'geojson',
            self.id_column,
            []
        )

        _ggq.assert_called_once_with(
            self.schema,
            self.table,
            'geojson',
            self.id_column,
            []
        )

        _pga.assert_called_once_with("generated_query", [])


class SampleQuery(CommonSetup):
    def test_call_build_sample_common(self):
        query = generate_query_sample(
            'PG',
            'SCHEMA',
            'TABLE',
            ['C1', 'C2']
        )

        self.assertEqual(
            query,
            'SELECT C1, C2 FROM SCHEMA.TABLE limit 10'
        )

    def test_call_build_sample_oracle(self):
        query = generate_query_sample(
            'ORA',
            'SCHEMA',
            'TABLE',
            ['C1', 'C2']
        )

        self.assertEqual(
            query,
            'SELECT C1, C2 FROM SCHEMA.TABLE WHERE rownum < 10'
        )

    def test_call_build_sample_common_no_limit(self):
        query = generate_query_sample(
            'PG',
            'SCHEMA',
            'TABLE',
            ['C1', 'C2'],
            limit=False
        )

        self.assertEqual(
            query,
            'SELECT C1, C2 FROM SCHEMA.TABLE'
        )

    def test_call_build_sample_oracle_no_limit(self):
        query = generate_query_sample(
            'ORA',
            'SCHEMA',
            'TABLE',
            ['C1', 'C2'],
            limit=False
        )

        self.assertEqual(
            query,
            'SELECT C1, C2 FROM SCHEMA.TABLE'
        )

    @mock.patch('lupa.db_connectors.postgres_access')
    def test_execute_sample_happypath(self, _pga):
        execute_sample(
            'PG',
            'SCHEMA',
            'TABLE',
            ['C1', 'C2']
        )

        _pga.assert_called_once_with(
            'SELECT C1, C2 FROM SCHEMA.TABLE limit 10',
            []
        )

    @mock.patch('lupa.db_connectors.postgres_access')
    def test_execute_sample_happypath_no_limit(self, _pga):
        execute_sample(
            'PG',
            'SCHEMA',
            'TABLE',
            ['C1', 'C2'],
            limit=False
        )

        _pga.assert_called_once_with(
            'SELECT C1, C2 FROM SCHEMA.TABLE',
            []
        )

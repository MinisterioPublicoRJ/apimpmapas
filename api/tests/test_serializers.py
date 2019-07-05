from unittest import TestCase, mock

import pytest

from model_mommy.mommy import make

from api.serializers import DadoSerializer


@pytest.mark.django_db(transaction=True)
class DadoSerializerTest(TestCase):
    def setUp(self):
        self.expected_query = 'SELECT col1, col2 FROM schema.tabela WHERE '\
                              'col_id = %s'
        self.db = 'PG'
        self.schema = 'schema'
        self.table = 'tabela'
        self.columns = ['col1', 'col2']
        self.id_column = 'col_id'
        self.domain_id = '00'

    @mock.patch('api.serializers.execute')
    def test_call_correct_database(self, _execute):

        dado_obj = make(
            'api.Dado',
            database=self.db,
            schema=self.schema,
            table=self.table,
            columns=self.columns,
            id_column=self.id_column
        )
        DadoSerializer(dado_obj, domain_id=self.domain_id).data

        _execute.assert_called_once_with(
            self.db,
            self.schema,
            self.table,
            self.columns,
            self.id_column,
            self.domain_id
        )

    @mock.patch('api.serializers.execute')
    def test_call_correct_query(self, _execute):
        expected_response = {'dado_teste': 00}

        _execute.return_value = expected_response

        dado_obj = make(
            'api.Dado',
            database=self.db,
            schema=self.schema,
            table=self.table,
            columns=self.columns,
            id_column=self.id_column
        )
        dado_ser = DadoSerializer(dado_obj, domain_id=self.domain_id).data

        _execute.assert_called_once_with(
            self.db,
            self.schema,
            self.table,
            self.columns,
            self.id_column,
            self.domain_id
        )
        self.assertEqual(dado_ser['external_data'], expected_response)
        for key in ['title', 'entity_type', 'database', 'query']:
            with self.subTest():
                self.assertNotIn(key, dado_ser)

from unittest import TestCase, mock

import pytest

from model_mommy.mommy import make

from api.serializers import DadoSerializer


@pytest.mark.django_db(transaction=True)
class DadoSerializerTest(TestCase):
    @mock.patch('api.serializers.execute')
    def test_call_correct_database(self, _execute):
        expected_query = 'SELECT "col1", "col2" FROM "schema"."tabela" WHERE "col_id" = 00'
        db = 'PG'
        schema = 'schema'
        table = 'tabela'
        columns = ['col1', 'col2']
        id_column = 'col_id'
        domain_id = '00'

        dado_obj = make(
            'api.Dado',
            database=db,
            schema=schema,
            table=table,
            columns=columns,
            id_column=id_column
        )
        DadoSerializer(dado_obj, domain_id=domain_id).data

        _execute.assert_called_once_with(
            db,
            schema,
            table,
            columns,
            id_column,
            domain_id
        )

    @mock.patch('api.serializers.execute')
    def test_call_correct_query(self, _execute):
        expected_response = {'dado_teste': 00}
        expected_query = 'SELECT "col1", "col2" FROM "schema"."tabela" WHERE "col_id" = 00'
        db = 'PG'
        schema = 'schema'
        table = 'tabela'
        columns = ['col1', 'col2']
        id_column = 'col_id'
        domain_id = '00'

        _execute.return_value = expected_response

        dado_obj = make(
            'api.Dado',
            database=db,
            schema=schema,
            table=table,
            columns=columns,
            id_column=id_column
        )
        dado_ser = DadoSerializer(dado_obj, domain_id=domain_id).data

        _execute.assert_called_once_with(
            db,
            schema,
            table,
            columns,
            id_column,
            domain_id
        )
        self.assertEqual(dado_ser['external_data'], expected_response)
        for key in ['title', 'entity_type', 'database', 'query']:
            with self.subTest():
                self.assertNotIn(key, dado_ser)

from unittest import TestCase, mock

import pytest

from model_mommy.mommy import make

from api.serializers import DadoSerializer


@pytest.mark.django_db(transaction=True)
class DadoSerializerTest(TestCase):
    @mock.patch('api.serializers.execute')
    def test_call_correct_database(self, _execute):
        query = 'SELECT * FROM TABELA'
        db = 'PG'
        domain_id = '33'

        dado_obj = make(
            'api.Dado',
            query=query,
            database=db
        )
        DadoSerializer(dado_obj, domain_id=domain_id).data

        _execute.assert_called_once_with(db, query, domain_id)

    @mock.patch('api.serializers.execute')
    def test_call_correct_query(self, _execute):
        expected_response = {'dado_teste': 32}
        query = 'SELECT * FROM TABELA'
        db = 'PG'
        domain_id = '33'

        _execute.return_value = expected_response

        dado_obj = make(
            'api.Dado',
            query=query,
            database=db
        )
        dado_ser = DadoSerializer(dado_obj, domain_id=domain_id).data

        _execute.assert_called_once_with(db, query, domain_id)
        self.assertEqual(dado_ser['external_data'], expected_response)
        for key in ['title', 'entity_type', 'database', 'query']:
            with self.subTest():
                self.assertNotIn(key, dado_ser)

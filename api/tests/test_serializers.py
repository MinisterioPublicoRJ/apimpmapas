from unittest import mock

from django.test import TestCase

from model_mommy.mommy import make

from api.serializers import DadoSerializer


class DataTypeViewTest(TestCase):
    @mock.patch('api.serializers.execute')
    def test_dado_list(self, _execute):
        _execute.return_value = [
            ('dado1', None, 'fonte', None, 'link1'),
            ('dado2', None, 'fonte', None, 'link2'),
            ('dado3', None, 'fonte', None, 'link3'),
        ]

        expected_value = [{
            'dado': 'dado1',
            'label': None,
            'fonte': 'fonte',
            'detalhes': None,
            'link': 'link1'
        }, {
            'dado': 'dado2',
            'label': None,
            'fonte': 'fonte',
            'detalhes': None,
            'link': 'link2'
        }, {
            'dado': 'dado3',
            'label': None,
            'fonte': 'fonte',
            'detalhes': None,
            'link': 'link3'
        }]

        dado = make('api.Dado', data_type='lista_sem_ordenacao')
        dado_ser = DadoSerializer(dado, domain_id='00').data

        self.assertEqual(dado_ser['external_data'], expected_value)

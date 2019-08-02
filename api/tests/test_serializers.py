from unittest import mock

from django.test import TestCase

from model_mommy.mommy import make

from api.serializers import DadoSerializer


class DataTypeViewTest(TestCase):

    def setUp(self):
        self.return_execute = [
            ('dado1', None, 'fonte', None, None, 'link1', None),
            ('dado2', None, 'fonte', None, None, 'link2', None),
            ('dado3', None, 'fonte', None, None, 'link3', None),
        ]
        self.expected_value = [{
            'dado': 'dado1',
            'rotulo': None,
            'fonte': 'fonte',
            'imagem': None,
            'detalhes': None,
            'link_interno_entidade': None,
            'link_interno_id': None,
            'link_externo': 'link1'
        }, {
            'dado': 'dado2',
            'rotulo': None,
            'fonte': 'fonte',
            'imagem': None,
            'detalhes': None,
            'link_interno_entidade': None,
            'link_interno_id': None,
            'link_externo': 'link2'
        }, {
            'dado': 'dado3',
            'rotulo': None,
            'fonte': 'fonte',
            'imagem': None,
            'detalhes': None,
            'link_interno_entidade': None,
            'link_interno_id': None,
            'link_externo': 'link3'
        }]

    @mock.patch('api.serializers.execute')
    def test_dado_list(self, _execute):
        _execute.return_value = self.return_execute

        dado = make('api.Dado', data_type='lista_sem_ordenacao')
        dado_ser = DadoSerializer(dado, domain_id='00').data

        self.assertEqual(dado_ser['external_data'], self.expected_value)

    @mock.patch('api.serializers.execute')
    def test_dado_graph(self, _execute):
        _execute.return_value = self.return_execute

        dado = make('api.Dado', data_type='grafico_barra_vertical')
        dado_ser = DadoSerializer(dado, domain_id='00').data

        self.assertEqual(dado_ser['external_data'], self.expected_value)

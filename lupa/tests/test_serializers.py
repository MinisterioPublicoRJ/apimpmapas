from unittest import mock

from django.test import TestCase

from model_mommy.mommy import make

from lupa.models import TipoDado
from lupa.serializers import DadoSerializer


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

    @mock.patch('lupa.serializers.execute')
    def test_dado_list(self, _execute):
        _execute.return_value = self.return_execute

        tipo_dado = make(
            'lupa.TipoDado',
            name='lista_sem_ordenacao',
            serialization=TipoDado.LIST_DATA
        )
        dado = make('lupa.Dado', data_type=tipo_dado)
        dado_ser = DadoSerializer(dado, domain_id='00').data

        self.assertEqual(dado_ser['external_data'], self.expected_value)

    @mock.patch('lupa.serializers.execute')
    def test_dado_list_limit(self, _execute):
        _execute.return_value = self.return_execute
        fetch = 2

        tipo_dado = make(
            'lupa.TipoDado',
            name='lista_sem_ordenacao',
            serialization=TipoDado.LIST_DATA
        )

        dado = make(
            'lupa.Dado',
            data_type=tipo_dado,
            limit_fetch=fetch
        )
        dado_ser = DadoSerializer(dado, domain_id='00').data

        self.assertEqual(
            dado_ser['external_data'],
            self.expected_value[:fetch]
        )

    @mock.patch('lupa.serializers.execute')
    def test_dado_graph(self, _execute):
        _execute.return_value = self.return_execute

        tipo_dado = make(
            'lupa.TipoDado',
            name='grafico_barra_vertical',
            serialization=TipoDado.XY_GRAPH_DATA
        )
        dado = make('lupa.Dado', data_type=tipo_dado)
        dado_ser = DadoSerializer(dado, domain_id='00').data

        self.assertEqual(dado_ser['external_data'], self.expected_value)

    @mock.patch('lupa.serializers.execute')
    def test_dado_graph_outros(self, _execute):
        _execute.return_value = [
            (70, 'dado1', 'fonte', None, None, 'link1', None),
            (25, 'dado2', 'fonte', None, None, 'link2', None),
            (1, 'dado3', 'fonte', None, None, 'link3', None),
            (1, 'dado4', 'fonte', None, None, 'link4', None),
            (1, 'dado5', 'fonte', None, None, 'link5', None),
            (1, 'dado6', 'fonte', None, None, 'link6', None),
            (1, 'dado7', 'fonte', None, None, 'link7', None),
        ]

        expected_value = [{
            'dado': 70,
            'rotulo': 'dado1',
            'fonte': 'fonte',
            'imagem': None,
            'detalhes': None,
            'link_interno_entidade': None,
            'link_interno_id': None,
            'link_externo': 'link1'
        }, {
            'dado': 25,
            'rotulo': 'dado2',
            'fonte': 'fonte',
            'imagem': None,
            'detalhes': None,
            'link_interno_entidade': None,
            'link_interno_id': None,
            'link_externo': 'link2'
        }, {
            'dado': 5,
            'rotulo': 'Outros',
            'fonte': 'fonte',
            'imagem': None,
            'detalhes': None,
            'link_interno_entidade': None,
            'link_interno_id': None,
            'link_externo': None
        }]

        tipo_dado = make(
            'lupa.TipoDado',
            name='grafico_pizza',
            serialization=TipoDado.PIZZA_GRAPH_DATA
        )
        dado = make('lupa.Dado', data_type=tipo_dado)
        dado_ser = DadoSerializer(dado, domain_id='00').data

        self.assertEqual(dado_ser['external_data'], expected_value)

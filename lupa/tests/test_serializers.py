from unittest import mock

from django.test import TestCase

from model_mommy.mommy import make

from lupa.models import TipoDado
from lupa.serializers import DadoEntidadeSerializer


class DataTypeViewTest(TestCase):

    def setUp(self):
        self.return_execute = [
            ('dado1', 'rotulo1', 'fonte', 'link1'),
            ('dado2', 'rotulo2', 'fonte', 'link2'),
            ('dado3', 'rotulo3', 'fonte', 'link3'),
        ]
        self.expected_value = [{
            'dado': 'dado1',
            'rotulo': 'rotulo1',
            'fonte': 'fonte',
            'link_externo': 'link1'
        }, {
            'dado': 'dado2',
            'rotulo': 'rotulo2',
            'fonte': 'fonte',
            'link_externo': 'link2'
        }, {
            'dado': 'dado3',
            'rotulo': 'rotulo3',
            'fonte': 'fonte',
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
        dado = make('lupa.DadoEntidade', data_type=tipo_dado)
        make('lupa.ColunaDado', info_type='link_externo', name='ln', dado=dado)
        make('lupa.ColunaDado', info_type='fonte', name='fon', dado=dado)
        make('lupa.ColunaDado', info_type='rotulo', name='lb', dado=dado)
        make('lupa.ColunaDado', info_type='dado', name='data', dado=dado)
        dado_ser = DadoEntidadeSerializer(dado, domain_id='00').data

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
            'lupa.DadoEntidade',
            data_type=tipo_dado,
            limit_fetch=fetch
        )
        make('lupa.ColunaDado', info_type='link_externo', name='ln', dado=dado)
        make('lupa.ColunaDado', info_type='fonte', name='fon', dado=dado)
        make('lupa.ColunaDado', info_type='rotulo', name='lb', dado=dado)
        make('lupa.ColunaDado', info_type='dado', name='data', dado=dado)
        dado_ser = DadoEntidadeSerializer(dado, domain_id='00').data

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
        dado = make('lupa.DadoEntidade', data_type=tipo_dado)
        make('lupa.ColunaDado', info_type='link_externo', name='ln', dado=dado)
        make('lupa.ColunaDado', info_type='fonte', name='fon', dado=dado)
        make('lupa.ColunaDado', info_type='rotulo', name='fon', dado=dado)
        make('lupa.ColunaDado', info_type='dado', name='data', dado=dado)
        dado_ser = DadoEntidadeSerializer(dado, domain_id='00').data

        self.assertEqual(dado_ser['external_data'], self.expected_value)

    @mock.patch('lupa.serializers.execute')
    def test_dado_graph_outros(self, _execute):
        _execute.return_value = [
            (70, 'dado1', 'fonte', 'link1'),
            (25, 'dado2', 'fonte', 'link2'),
            (1, 'dado3', 'fonte', 'link3'),
            (1, 'dado4', 'fonte', 'link4'),
            (1, 'dado5', 'fonte', 'link5'),
            (1, 'dado6', 'fonte', 'link6'),
            (1, 'dado7', 'fonte', 'link7'),
        ]

        expected_value = [{
            'dado': 70,
            'rotulo': 'dado1',
            'fonte': 'fonte',
            'link_externo': 'link1'
        }, {
            'dado': 25,
            'rotulo': 'dado2',
            'fonte': 'fonte',
            'link_externo': 'link2'
        }, {
            'dado': 5,
            'rotulo': 'Outros'
        }]

        tipo_dado = make(
            'lupa.TipoDado',
            name='grafico_pizza',
            serialization=TipoDado.PIZZA_GRAPH_DATA
        )
        dado = make('lupa.DadoEntidade', data_type=tipo_dado)
        make('lupa.ColunaDado', info_type='link_externo', name='ln', dado=dado)
        make('lupa.ColunaDado', info_type='fonte', name='fon', dado=dado)
        make('lupa.ColunaDado', info_type='rotulo', name='fon', dado=dado)
        make('lupa.ColunaDado', info_type='dado', name='data', dado=dado)
        dado_ser = DadoEntidadeSerializer(dado, domain_id='00').data

        self.assertEqual(dado_ser['external_data'], expected_value)

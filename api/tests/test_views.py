from unittest import mock
from django.test import TestCase
from django.urls import reverse

from model_mommy.mommy import make


class EntidadeViewTest(TestCase):

    def test_entidade_ok(self):
        expected_answer = {
            'id': 2,
            'data_list': [
                {'id': 1},
                {'id': 7},
            ],
            'domain_id': '33',
            'exibition_field': 'Rio de Janeiro',
            'entity_type': 'Estado'
        }

        make(
            'api.Entidade',
            id=2,
            entity_type='EST',
            exibition_field='Rio de Janeiro',
            domain_id=33
        )

        make('api.Dado', id=1, entity_type='EST')
        make('api.Dado', id=7, entity_type='EST')
        make('api.Dado', id=9, entity_type='MUN')

        url = reverse('api:detail_entidade', args=('EST', '33',))

        resp = self.client.get(url)
        resp_json = resp.json()

        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp_json, expected_answer)

    def test_entidade_nao_existente(self):
        make('api.Entidade', entity_type='MUN', domain_id=404)

        url = reverse('api:detail_entidade', args=('MUN', '1',))

        resp = self.client.get(url)

        self.assertEqual(resp.status_code, 404)


class ListDadosViewTest(TestCase):
    def test_get_lista_dados(self):
        """Deve retornar dados referentes ao tipo de entidade chamado"""
        make('api.Entidade', entity_type='MUN', domain_id=1)
        make('api.Dado', entity_type='EST', _quantity=2)
        dado_object_mun = make('api.Dado', entity_type='MUN', _quantity=2)

        url = reverse('api:detail_entidade', args=('MUN', '1',))

        resp = self.client.get(url)
        resp_json = resp.json()

        self.assertEqual(resp.status_code, 200)
        self.assertEqual(
            len(resp_json['data_list']),
            2
        )
        self.assertEqual(
            resp_json['data_list'][0]['id'],
            dado_object_mun[0].id
        )
        self.assertEqual(
            resp_json['data_list'][1]['id'],
            dado_object_mun[1].id
        )


class DetailDadosViewTest(TestCase):

    def setUp(self):
        self.data_id = 7
        self.data_id_alt = 9
        self.external_data = '202'
        self.external_source = 'http://mca.mp.rj.gov.br/'
        self.external_description = None
        self.exibition_field = 'Abrigos para crianças e adolescentes'
        self.domain_id = '33'
        self.entity_type = 'EST'
        self.text_type = 'TEX_PEQ_DEST'
        self.text_response = 'texto_pequeno_destaque'

    @mock.patch('api.serializers.execute')
    def test_dado_ok(self, _execute):
        expected_response = {
            'id': self.data_id,
            'external_data': {
                'dado': self.external_data,
                'fonte': self.external_source,
                'descricao': self.external_description
            },
            'exibition_field': self.exibition_field,
            'data_type': self.text_response
        }

        _execute.return_value = [(
            self.external_data,
            self.external_source,
            self.external_description
        )]

        make(
            'api.Dado',
            id=self.data_id,
            data_type=self.text_type,
            entity_type=self.entity_type,
            exibition_field=self.exibition_field
        )

        url = reverse(
            'api:detail_dado',
            args=(self.entity_type, self.domain_id, self.data_id)
        )
        resp = self.client.get(url)
        resp_json = resp.json()

        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp_json, expected_response)

    @mock.patch('api.serializers.execute')
    def test_dado_sem_retorno_db(self, _execute):
        _execute.return_value = []

        make(
            'api.Dado',
            id=self.data_id,
            data_type=self.text_type,
            entity_type=self.entity_type,
            exibition_field=self.exibition_field
        )

        url = reverse(
            'api:detail_dado',
            args=(self.entity_type, self.domain_id, self.data_id)
        )
        resp = self.client.get(url)

        self.assertEqual(resp.status_code, 404)

    def test_dado_nao_existente(self):
        make(
            'api.Dado',
            id=self.data_id_alt,
            data_type=self.text_type,
            entity_type=self.entity_type,
            exibition_field=self.exibition_field
        )

        url = reverse(
            'api:detail_dado',
            args=(self.entity_type, self.domain_id, self.data_id)
        )
        resp = self.client.get(url)

        self.assertEqual(resp.status_code, 404)

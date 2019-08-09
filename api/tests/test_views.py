from unittest import mock

from django.conf import settings
from django.test import TestCase
from django.urls import reverse

from model_mommy.mommy import make

from api.exceptions import QueryError


class EntidadeViewTest(TestCase):

    @mock.patch('api.serializers.execute')
    def test_entidade_ok(self, _execute):
        expected_answer = {
            'domain_id': '33',
            'entity_type': 'Estado',
            'exibition_field': 'Rio de Janeiro',
            'geojson': None,
            'theme_list': [
                {
                    'tema': None,
                    'cor': None,
                    'data_list': [
                        {'id': 4}
                    ]
                },
                {
                    'tema': 'Segurança',
                    'cor': '#223478',
                    'data_list': [
                        {'id': 1},
                        {'id': 7}
                    ]
                },
                {
                    'tema': None,
                    'cor': None,
                    'data_list': [
                        {'id': 8},
                        {'id': 2}
                    ]
                },
                {
                    'tema': 'Saúde',
                    'cor': '#223578',
                    'data_list': [
                        {'id': 5}
                    ]
                }
            ]
        }

        _execute.return_value = [('Rio de Janeiro', 'mock_geo')]

        estado = make('api.Entidade', name='Estado', abreviation='EST')
        municipio = make('api.Entidade', abreviation='MUN')

        seguranca = make('api.TemaDado', name='Segurança', color='#223478')
        saude = make('api.TemaDado', name='Saúde', color='#223578')

        make('api.Dado', id=1, entity_type=estado, theme=seguranca, order=2)
        make('api.Dado', id=2, entity_type=estado, theme=None, order=5)
        make('api.Dado', id=3, entity_type=municipio, order=7)
        make('api.Dado', id=4, entity_type=estado, theme=None, order=1)
        make('api.Dado', id=5, entity_type=estado, theme=saude, order=8)
        make('api.Dado', id=6, entity_type=municipio, order=6)
        make('api.Dado', id=7, entity_type=estado, theme=seguranca, order=3)
        make('api.Dado', id=8, entity_type=estado, theme=None, order=4)

        url = reverse('api:detail_entidade', args=('EST', '33',))

        resp = self.client.get(url)
        resp_json = resp.json()
        # import ipdb; ipdb.set_trace()

        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp_json, expected_answer)

    @mock.patch('api.serializers.execute')
    def test_entidade_nao_existente(self, _execute):
        make('api.Entidade', abreviation='MUN')
        _execute.return_value = []

        url = reverse('api:detail_entidade', args=('MUN', '1',))

        resp = self.client.get(url)

        self.assertEqual(resp.status_code, 404)

    @mock.patch('api.serializers.execute')
    def test_entidade_com_erro(self, _execute):
        _execute.side_effect = QueryError('test error')

        make('api.Entidade', id=1, abreviation='MUN')
        url = reverse('api:detail_entidade', args=('MUN', '1',))
        resp = self.client.get(url)

        self.assertEqual(resp.status_code, 404)


class ListDadosViewTest(TestCase):

    @mock.patch('api.serializers.execute')
    def test_get_lista_dados(self, _execute):
        """Deve retornar dados referentes ao tipo de entidade chamado"""
        _execute.side_effect = [
            [('mock_name', )],
            None,
        ]

        ent_estado = make('api.Entidade', abreviation='EST')
        ent_municipio = make('api.Entidade', abreviation='MUN')

        make('api.Dado', entity_type=ent_estado, _quantity=2)
        dado_object_mun_0 = make(
            'api.Dado',
            entity_type=ent_municipio,
            theme=None,
            order=1
        )
        dado_object_mun_1 = make(
            'api.Dado',
            entity_type=ent_municipio,
            theme=None,
            order=2
        )
        expected_datalist = [
            {"id": dado_object_mun_0.id},
            {"id": dado_object_mun_1.id}
        ]

        url = reverse('api:detail_entidade', args=('MUN', '1',))

        resp = self.client.get(url)
        resp_json = resp.json()

        self.assertEqual(resp.status_code, 200)
        self.assertEqual(len(resp_json['theme_list'][0]['data_list']), 2)
        self.assertEqual(
            resp_json['theme_list'][0]['data_list'],
            expected_datalist
        )


class DetailDadosViewTest(TestCase):

    def setUp(self):
        self.entity_id = 1
        self.entity_abrv = 'EST'
        self.data_id = 7
        self.data_id_alt = 9
        self.external_data = '202'
        self.external_source = 'http://mca.mp.rj.gov.br/'
        self.external_description = None
        self.external_label = None
        self.external_link = None
        self.exibition_field = 'Abrigos para crianças e adolescentes'
        self.domain_id = '33'
        self.external_entity = None
        self.external_ent_id = None
        self.icon_file = 'icones/python.svg'
        self.image = None

        self.data_type = 'texto_pequeno_destaque'
        self.data_type_obj = make(
            'api.TipoDado',
            name=self.data_type,
            serialization='Singleton'
        )

    @mock.patch('api.serializers.execute')
    def test_dado_ok(self, _execute):

        expected_response = {
            'id': self.data_id,
            'external_data': {
                'dado': self.external_data,
                'rotulo': self.external_label,
                'fonte': self.external_source,
                'imagem': self.image,
                'detalhes': self.external_description,
                'link_interno_entidade': self.external_entity,
                'link_interno_id': self.external_ent_id,
                'link_externo': self.external_link
            },
            'exibition_field': self.exibition_field,
            'data_type': self.data_type,
            'icon': settings.MEDIA_URL + self.icon_file
        }

        _execute.return_value = [(
            self.external_data,
            self.external_label,
            self.external_source,
            self.external_description,
            self.external_ent_id,
            self.external_link,
            self.image
        )]

        entidade = make(
            'api.Entidade',
            id=self.entity_id,
            abreviation=self.entity_abrv,
        )
        make(
            'api.Dado',
            id=self.data_id,
            data_type=self.data_type_obj,
            entity_type=entidade,
            exibition_field=self.exibition_field,
            icon__file_path=self.icon_file
        )

        url = reverse(
            'api:detail_dado',
            args=(self.entity_abrv, self.domain_id, self.data_id)
        )
        resp = self.client.get(url)
        resp_json = resp.json()

        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp_json, expected_response)

    @mock.patch('api.serializers.execute')
    def test_dado_sem_retorno_db(self, _execute):
        _execute.return_value = []

        entidade = make(
            'api.Entidade',
            id=self.entity_id,
            abreviation=self.entity_abrv,
        )

        make(
            'api.Dado',
            id=self.data_id,
            entity_type=entidade,
            data_type=self.data_type_obj
        )

        url = reverse(
            'api:detail_dado',
            args=(self.entity_abrv, self.domain_id, self.data_id)
        )
        resp = self.client.get(url)

        self.assertEqual(resp.status_code, 404)

    def test_dado_nao_existente(self):
        entidade = make(
            'api.Entidade',
            id=self.entity_id,
            abreviation=self.entity_abrv,
        )
        make(
            'api.Dado',
            id=self.data_id_alt,
            entity_type=entidade
        )

        url = reverse(
            'api:detail_dado',
            args=(self.entity_abrv, self.domain_id, self.data_id)
        )
        resp = self.client.get(url)

        self.assertEqual(resp.status_code, 404)

    @mock.patch('api.serializers.execute')
    def test_dado_com_erro(self, _execute):
        _execute.side_effect = QueryError('test error')

        entidade = make(
            'api.Entidade',
            id=self.entity_id,
            abreviation=self.entity_abrv,
        )
        make(
            'api.Dado',
            id=self.data_id,
            entity_type=entidade
        )

        url = reverse(
            'api:detail_dado',
            args=(self.entity_abrv, self.domain_id, self.data_id)
        )
        resp = self.client.get(url)

        self.assertEqual(resp.status_code, 404)

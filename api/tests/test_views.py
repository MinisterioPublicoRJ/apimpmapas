from unittest import mock

from django.conf import settings
from django.test import TestCase
from django.urls import reverse

from model_mommy.mommy import make

from api.exceptions import QueryError


def mock_config(*args, **kwargs):
    if args[0] == 'SECRET_KEY':
        return 'sfdfsdf'


class LoggedClient:
    def __init__(self, client):
        self.client = client

    def get(self, url):
        token = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9'\
                '.eyJ1aWQiOiJFc3RldmFuIn0'\
                '.QsoGOa0S89KYUUpuwQ-QPq9cSSpuJdvxa3zYBeWcN1o'
        url += '?auth_token=' + token

        with mock.patch('login.decorators.config', side_effect=mock_config):
            return self.client.get(url)


class EntidadeViewTest(TestCase):
    def setUp(self):
        self.logged_client = LoggedClient(self.client)

    @mock.patch('api.serializers.execute')
    def test_entidade_ok(self, _execute):
        expected_answer = {
            'domain_id': '33',
            'entity_type': 'Estado',
            'exibition_field': 'Rio de Janeiro',
            'geojson': None,
            'data_list': [
                {'id': 1},
                {'id': 7},
            ]
        }

        _execute.return_value = [('Rio de Janeiro', 'mock_geo')]

        estado = make('api.Entidade', name='Estado', abreviation='EST')
        municipio = make('api.Entidade', abreviation='MUN')

        make('api.Dado', id=1, entity_type=estado, order=1)
        make('api.Dado', id=7, entity_type=estado, order=3)
        make('api.Dado', id=9, entity_type=municipio, order=2)

        url = reverse('api:detail_entidade', args=('EST', '33',))
        resp = self.logged_client.get(url)

        resp_json = resp.json()

        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp_json, expected_answer)

    @mock.patch('api.serializers.execute')
    def test_entidade_nao_existente(self, _execute):
        make('api.Entidade', abreviation='MUN')
        _execute.return_value = []

        url = reverse('api:detail_entidade', args=('MUN', '1',))

        resp = self.logged_client.get(url)

        self.assertEqual(resp.status_code, 404)

    @mock.patch('api.serializers.execute')
    def test_entidade_com_erro(self, _execute):
        _execute.side_effect = QueryError('test error')

        make('api.Entidade', id=1, abreviation='MUN')
        url = reverse('api:detail_entidade', args=('MUN', '1',))
        resp = self.logged_client.get(url)

        self.assertEqual(resp.status_code, 404)


class ListDadosViewTest(TestCase):
    def setUp(self):
        self.logged_client = LoggedClient(self.client)

    @mock.patch('api.serializers.execute')
    def test_get_lista_dados(self, _execute):
        """Deve retornar dados referentes ao tipo de entidade chamado"""
        _execute.return_value = [('mock_name', 'mock_geo')]

        ent_estado = make('api.Entidade', abreviation='EST')
        ent_municipio = make('api.Entidade', abreviation='MUN')

        make('api.Dado', entity_type=ent_estado, _quantity=2)
        dado_object_mun_0 = make(
            'api.Dado',
            entity_type=ent_municipio,
            order=1
        )
        dado_object_mun_1 = make(
            'api.Dado',
            entity_type=ent_municipio,
            order=2
        )
        expected_datalist = [
            {"id": dado_object_mun_0.id},
            {"id": dado_object_mun_1.id}
        ]

        url = reverse('api:detail_entidade', args=('MUN', '1',))

        resp = self.logged_client.get(url)
        resp_json = resp.json()

        # import pdb; pdb.set_trace()

        self.assertEqual(resp.status_code, 200)
        self.assertEqual(len(resp_json['data_list']), 2)
        self.assertEqual(
            resp_json['data_list'],
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
        self.exibition_field = 'Abrigos para crianças e adolescentes'
        self.domain_id = '33'
        self.text_type = 'texto_pequeno_destaque'
        self.icon_file = 'icones/python.svg'

        self.logged_client = LoggedClient(self.client)

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
            'data_type': self.text_type,
            'icon': settings.MEDIA_URL + self.icon_file
        }

        _execute.return_value = [(
            self.external_data,
            self.external_source,
            self.external_description
        )]

        entidade = make(
            'api.Entidade',
            id=self.entity_id,
            abreviation=self.entity_abrv,
        )
        make(
            'api.Dado',
            id=self.data_id,
            data_type=self.text_type,
            entity_type=entidade,
            exibition_field=self.exibition_field,
            icon__file_path=self.icon_file
        )

        url = reverse(
            'api:detail_dado',
            args=(self.entity_abrv, self.domain_id, self.data_id)
        )
        resp = self.logged_client.get(url)
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
            data_type=self.text_type,
            entity_type=entidade,
            exibition_field=self.exibition_field
        )

        url = reverse(
            'api:detail_dado',
            args=(self.entity_abrv, self.domain_id, self.data_id)
        )
        resp = self.logged_client.get(url)

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
            data_type=self.text_type,
            entity_type=entidade,
            exibition_field=self.exibition_field
        )

        url = reverse(
            'api:detail_dado',
            args=(self.entity_abrv, self.domain_id, self.data_id)
        )
        resp = self.logged_client.get(url)

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
            data_type=self.text_type,
            entity_type=entidade,
            exibition_field=self.exibition_field
        )

        url = reverse(
            'api:detail_dado',
            args=(self.entity_abrv, self.domain_id, self.data_id)
        )
        resp = self.logged_client.get(url)

        self.assertEqual(resp.status_code, 404)


class EndpointsAuthentication(TestCase):
    def setUp(self):
        self.logged_client = LoggedClient(self.client)

    @mock.patch('api.serializers.execute')
    def test_not_logged_in_detail_entidade(self, _execute):
        url = reverse('api:detail_entidade', args=('EST', '33',))

        resp = self.client.get(url)

        self.assertEqual(resp.status_code, 403)

    @mock.patch('api.serializers.execute')
    def test_not_logged_in_detail_dado(self, _execute):
        domain_id = 1
        entity_abrv = 'EST'
        data_id = 7
        url = reverse(
            'api:detail_dado',
            args=(entity_abrv, domain_id, data_id)
        )

        resp = self.client.get(url)

        self.assertEqual(resp.status_code, 403)

    @mock.patch('api.views.EntidadeSerializer')
    @mock.patch('api.views.get_object_or_404', return_value=[])
    @mock.patch('api.serializers.execute')
    def test_logged_in_detail_entidade(self, _execute, _get_obj, _ser):
        mock_obj = mock.MagicMock()
        mock_obj.data = {'exibition_field': 1}
        _ser.return_value = mock_obj
        url = reverse('api:detail_entidade', args=('EST', '33',))
        resp = self.logged_client.get(url)

        self.assertEqual(resp.status_code, 200)

    @mock.patch('api.views.DadoSerializer')
    @mock.patch('api.views.get_object_or_404', return_value=[])
    @mock.patch('api.serializers.execute')
    def test_logged_in_detail_dado(self, _execute, _get_obj, _ser):
        mock_obj = mock.MagicMock()
        mock_obj.data = {'external_data': 1}
        _ser.return_value = mock_obj

        domain_id = 1
        entity_abrv = 'EST'
        data_id = 7

        url = reverse(
            'api:detail_dado',
            args=(entity_abrv, domain_id, data_id)
        )

        resp = self.logged_client.get(url)

        self.assertEqual(resp.status_code, 200)

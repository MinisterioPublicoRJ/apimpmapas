from unittest import mock

from decouple import config
from django.conf import settings
from django.core.cache import cache
from django.test import TestCase
from django.urls import reverse
import jwt
import pytest
from model_mommy.mommy import make
import responses

from lupa.exceptions import QueryError
from lupa import osmapi
from .fixtures.osmapi import default_response


class NoCacheTestCase:
    def teardown_method(self, method):
        cache.clear()


class EntidadeViewTest(TestCase):

    @mock.patch('lupa.serializers.execute')
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

        estado = make('lupa.Entidade', name='Estado', abreviation='EST')
        municipio = make('lupa.Entidade', abreviation='MUN')

        seguranca = make('lupa.TemaDado', name='Segurança', color='#223478')
        saude = make('lupa.TemaDado', name='Saúde', color='#223578')

        make('lupa.Dado', id=1, entity_type=estado, theme=seguranca, order=2)
        make('lupa.Dado', id=2, entity_type=estado, theme=None, order=5)
        make('lupa.Dado', id=3, entity_type=municipio, order=7)
        make('lupa.Dado', id=4, entity_type=estado, theme=None, order=1)
        make('lupa.Dado', id=5, entity_type=estado, theme=saude, order=8)
        make('lupa.Dado', id=6, entity_type=municipio, order=6)
        make('lupa.Dado', id=7, entity_type=estado, theme=seguranca, order=3)
        make('lupa.Dado', id=8, entity_type=estado, theme=None, order=4)

        url = reverse('lupa:detail_entidade', args=('EST', '33',))

        resp = self.client.get(url)
        resp_json = resp.json()

        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp_json, expected_answer)

    @mock.patch('lupa.serializers.execute')
    def test_entidade_nao_existente(self, _execute):
        make('lupa.Entidade', abreviation='MUN')
        _execute.return_value = []

        url = reverse('lupa:detail_entidade', args=('MUN', '1',))

        resp = self.client.get(url)

        self.assertEqual(resp.status_code, 404)

    @mock.patch('lupa.serializers.execute')
    def test_entidade_com_erro(self, _execute):
        _execute.side_effect = QueryError('test error')

        make('lupa.Entidade', id=1, abreviation='MUN')
        url = reverse('lupa:detail_entidade', args=('MUN', '1',))
        resp = self.client.get(url)

        self.assertEqual(resp.status_code, 404)


class AuthEntidadeViewTest(TestCase):

    def setUp(self):
        self.role_allowed = 'role_allowed'
        self.role_forbidden = 'role_not_allowed'
        self.entity_abrv = 'EST'
        self.entity_type = 'Estado'
        self.entity_name = 'Rio de Janeiro'
        self.entity_id = '1'

        self.grupo_allowed = make(
            'lupa.Grupo',
            role=self.role_allowed
        )
        self.entidade = make(
            'lupa.Entidade',
            id=self.entity_id,
            roles_allowed=[self.grupo_allowed],
            name=self.entity_type,
            abreviation=self.entity_abrv
        )

    @mock.patch('lupa.serializers.execute')
    def test_entidade_permission_ok(self, _execute):
        payload = {'permissions': [self.role_allowed]}
        token = jwt.encode(payload, config('SECRET_KEY'), algorithm="HS256")

        _execute.return_value = [(self.entity_name, 'mock_geo')]

        url = reverse(
            'lupa:detail_entidade',
            args=(self.entity_abrv, self.entity_id)
        )
        resp = self.client.get(url, {'auth_token': token})
        resp_json = resp.json()

        expected_response = {
            'domain_id': self.entity_id,
            'entity_type': self.entity_type,
            'exibition_field': self.entity_name,
            'geojson': None,
            'theme_list': []
        }

        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp_json, expected_response)

    def test_entidade_missing_token(self):
        url = reverse(
            'lupa:detail_entidade',
            args=(self.entity_abrv, self.entity_id)
        )
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 403)

    def test_entidade_permission_failed(self):
        payload = {'permissions': [self.role_forbidden]}
        token = jwt.encode(payload, config('SECRET_KEY'), algorithm="HS256")

        url = reverse(
            'lupa:detail_entidade',
            args=(self.entity_abrv, self.entity_id)
        )
        resp = self.client.get(url, {'auth_token': token})
        self.assertEqual(resp.status_code, 403)


class ListDadosViewTest(TestCase, NoCacheTestCase):

    @mock.patch('lupa.serializers.execute')
    def test_get_lista_dados(self, _execute):
        """Deve retornar dados referentes ao tipo de entidade chamado"""
        _execute.side_effect = [
            [('mock_name', )],
            None,
        ]

        ent_estado = make('lupa.Entidade', abreviation='EST')
        ent_municipio = make('lupa.Entidade', abreviation='MUN')

        make('lupa.Dado', entity_type=ent_estado, _quantity=2)
        dado_object_mun_0 = make(
            'lupa.Dado',
            entity_type=ent_municipio,
            theme=None,
            order=1
        )
        dado_object_mun_1 = make(
            'lupa.Dado',
            entity_type=ent_municipio,
            theme=None,
            order=2
        )
        expected_datalist = [
            {"id": dado_object_mun_0.id},
            {"id": dado_object_mun_1.id}
        ]

        url = reverse('lupa:detail_entidade', args=('MUN', '1',))

        resp = self.client.get(url)
        resp_json = resp.json()

        self.assertEqual(resp.status_code, 200)
        self.assertEqual(len(resp_json['theme_list'][0]['data_list']), 2)
        self.assertEqual(
            resp_json['theme_list'][0]['data_list'],
            expected_datalist
        )

    @mock.patch('lupa.serializers.execute')
    def test_get_lista_com_dados_ocultos(self, _execute):
        """Deve retornar somente dados não ocultos referentes
 ao tipo de entidade chamado"""
        _execute.side_effect = [
            [('mock_name', )],
            None,
        ]

        ent_municipio = make('lupa.Entidade', abreviation='MUN')

        make(
            'lupa.Dado',
            entity_type=ent_municipio,
            show_box=False
        )
        dado_object_mun_1 = make(
            'lupa.Dado',
            entity_type=ent_municipio,
            theme=None,
            show_box=True
        )
        expected_datalist = [
            {"id": dado_object_mun_1.id}
        ]

        url = reverse('lupa:detail_entidade', args=('MUN', '1',))

        resp = self.client.get(url)
        resp_json = resp.json()

        self.assertEqual(resp.status_code, 200)
        self.assertEqual(len(resp_json['theme_list'][0]['data_list']), 1)
        self.assertEqual(
            resp_json['theme_list'][0]['data_list'],
            expected_datalist
        )


class DetailDadosViewTest(TestCase, NoCacheTestCase):

    def setUp(self):
        self.entity_id = 1
        self.entity_abrv = 'EST'
        self.data_id = 7
        self.data_id_alt = 9
        self.external_data = '202'
        self.external_source = 'http://mca.mp.rj.gov.br/'
        self.exibition_field = 'Abrigos para crianças e adolescentes'
        self.domain_id = '33'
        self.icon_file = 'icones/python.svg'

        self.data_type = 'texto_pequeno_destaque'
        self.data_type_obj = make(
            'lupa.TipoDado',
            name=self.data_type,
            serialization='Singleton'
        )

    @mock.patch('lupa.serializers.execute')
    def test_dado_ok(self, _execute):

        expected_response = {
            'id': self.data_id,
            'external_data': {
                'dado': self.external_data,
                'fonte': self.external_source,
                'id': self.data_id
            },
            'exibition_field': self.exibition_field,
            'data_type': self.data_type,
            'icon': settings.MEDIA_URL + self.icon_file
        }

        _execute.return_value = [(
            self.external_data,
            self.external_source,
            self.data_id
        )]

        entidade = make(
            'lupa.Entidade',
            id=self.entity_id,
            abreviation=self.entity_abrv,
        )
        dado = make(
            'lupa.Dado',
            id=self.data_id,
            data_type=self.data_type_obj,
            entity_type=entidade,
            exibition_field=self.exibition_field,
            icon__file_path=self.icon_file
        )
        make('lupa.ColunaDado', info_type='id', name='identi', dado=dado)
        make('lupa.ColunaDado', info_type='fonte', name='fon', dado=dado)
        make('lupa.ColunaDado', info_type='dado', name='data', dado=dado)

        url = reverse(
            'lupa:detail_dado',
            args=(self.entity_abrv, self.domain_id, self.data_id)
        )
        resp = self.client.get(url)
        resp_json = resp.json()

        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp_json, expected_response)

    @mock.patch('lupa.serializers.execute')
    def test_dado_sem_retorno_db(self, _execute):
        _execute.return_value = []

        entidade = make(
            'lupa.Entidade',
            id=self.entity_id,
            abreviation=self.entity_abrv,
        )

        make(
            'lupa.Dado',
            id=self.data_id,
            entity_type=entidade,
            data_type=self.data_type_obj
        )

        url = reverse(
            'lupa:detail_dado',
            args=(self.entity_abrv, self.domain_id, self.data_id)
        )
        resp = self.client.get(url)

        self.assertEqual(resp.status_code, 404)

    def test_dado_nao_existente(self):
        entidade = make(
            'lupa.Entidade',
            id=self.entity_id,
            abreviation=self.entity_abrv,
        )
        make(
            'lupa.Dado',
            id=self.data_id_alt,
            entity_type=entidade
        )

        url = reverse(
            'lupa:detail_dado',
            args=(self.entity_abrv, self.domain_id, self.data_id)
        )
        resp = self.client.get(url)

        self.assertEqual(resp.status_code, 404)

    @mock.patch('lupa.serializers.execute')
    def test_dado_com_erro(self, _execute):
        _execute.side_effect = QueryError('test error')

        entidade = make(
            'lupa.Entidade',
            id=self.entity_id,
            abreviation=self.entity_abrv,
        )
        make(
            'lupa.Dado',
            id=self.data_id,
            entity_type=entidade
        )

        url = reverse(
            'lupa:detail_dado',
            args=(self.entity_abrv, self.domain_id, self.data_id)
        )
        resp = self.client.get(url)

        self.assertEqual(resp.status_code, 404)


class AuthDadosViewTest(TestCase):

    def setUp(self):
        self.role_allowed = 'role_allowed'
        self.role_forbidden = 'role_not_allowed'
        self.entity_abrv = 'ENT'
        self.entity_id = 1
        self.data_id = 1
        self.dado_title = 'dado_teste'
        self.external_data = 'dado'
        self.data_type = 'texto_pequeno_destaque'

        self.data_type_obj = make(
            'lupa.TipoDado',
            name=self.data_type,
            serialization='Singleton'
        )
        self.entidade = make(
            'lupa.Entidade',
            id=self.entity_id,
            abreviation=self.entity_abrv
        )
        self.grupo_allowed = make(
            'lupa.Grupo',
            role=self.role_allowed
        )
        self.dado = make(
            'lupa.Dado',
            title=self.dado_title,
            roles_allowed=[self.grupo_allowed],
            id=self.data_id,
            entity_type=self.entidade,
            data_type=self.data_type_obj,
            make_m2m=True
        )
        make('lupa.ColunaDado', info_type='id', name='identi', dado=self.dado)
        make('lupa.ColunaDado', info_type='dado', name='data', dado=self.dado)

    @mock.patch('lupa.serializers.execute')
    def test_dado_permission_ok(self, _execute):
        payload = {'permissions': [self.role_allowed]}
        token = jwt.encode(payload, config('SECRET_KEY'), algorithm="HS256")

        _execute.return_value = [(
            self.external_data,
            self.data_id
        )]

        url = reverse(
            'lupa:detail_dado',
            args=(self.entity_abrv, self.entity_id, self.data_id)
        )
        resp = self.client.get(url, {'auth_token': token})
        resp_json = resp.json()

        expected_response = {
            'id': self.data_id,
            'icon': None,
            'exibition_field': None,
            'data_type': self.data_type,
            'external_data': {
                'dado': self.external_data,
                'id': self.data_id
            }
        }

        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp_json, expected_response)

    def test_dado_missing_token(self):
        url = reverse(
            'lupa:detail_dado',
            args=(self.entity_abrv, self.entity_id, self.data_id)
        )
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 403)

    def test_dado_permission_failed(self):
        payload = {'permissions': [self.role_forbidden]}
        token = jwt.encode(payload, config('SECRET_KEY'), algorithm="HS256")

        url = reverse(
            'lupa:detail_dado',
            args=(self.entity_abrv, self.entity_id, self.data_id)
        )
        resp = self.client.get(url, {'auth_token': token})
        self.assertEqual(resp.status_code, 403)


class OsmQueryViewTest(TestCase):

    @responses.activate
    def test_query_return(self):
        responses.add(
            "GET",
            osmapi.OSM_APY,
            json=default_response
        )
        url = reverse(
            'lupa:mapsearch',
            args=('tijuca',)
        )

        resp = self.client.get(url).json()
        self.assertEqual(len(resp), 3)

    @responses.activate
    @mock.patch('lupa.views.osmquery', return_value=[])
    def test_query_correct_parameter(self, _query):
        parameters = 'tijuquistão do norte  xablauzinho'
        responses.add(
            "GET",
            osmapi.OSM_APY,
            json=default_response
        )
        url = reverse(
            'lupa:mapsearch',
            args=(parameters,)
        )

        self.client.get(url).json()

        _query.assert_called_once_with(parameters)


@pytest.mark.django_db(transaction=True)
class GeoSpatialQueryViewTest(TestCase, NoCacheTestCase):

    @mock.patch('lupa.views.execute_geospatial', return_value=((33345,),))
    def test_happy_path(self, _egsp):
        make(
            'lupa.Entidade',
            abreviation='MUN',
            geojson_column="geojson_column",
            osm_value_attached="municipality",
        )
        make(
            'lupa.Entidade',
            abreviation='BAI',
            geojson_column="geojson_column",
            osm_value_attached="suburb",
        )

        url = reverse(
            "lupa:geospatial_entity",
            kwargs={
                'lat': '-22.000',
                'lon': '-43.000',
                'value': 'municipality'
            }
        )

        response = self.client.get(url).json()

        self.assertEqual(response['abreviation'], 'MUN')
        self.assertEqual(response['entity_id'], '33345')
        _egsp.assert_called()

    @mock.patch('lupa.views.execute_geospatial', return_value=((33345,),))
    def test_no_entity_responsible(self, _egsp):
        make(
            'lupa.Entidade',
            abreviation='MUN',
            geojson_column="geojson_column",
            osm_value_attached="municipality",
            osm_default_level=False
        )
        make(
            'lupa.Entidade',
            abreviation='BAI',
            geojson_column="geojson_column",
            osm_value_attached="suburb",
            osm_default_level=False
        )

        url = reverse(
            "lupa:geospatial_entity",
            kwargs={
                'lat': '-22.000',
                'lon': '-43.000',
                'value': 'house'
            }
        )

        _egsp.assert_not_called()

        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    @mock.patch(
        'lupa.views.execute_geospatial',
        return_value=(('minhacasa',),))
    def test_default_entity_responsible(self, _egsp):
        make(
            'lupa.Entidade',
            abreviation='MUN',
            geojson_column="geojson_column",
            osm_value_attached="municipality",
            osm_default_level=False
        )
        make(
            'lupa.Entidade',
            abreviation='BAI',
            geojson_column="geojson_column",
            osm_value_attached="suburb",
            osm_default_level=True
        )

        url = reverse(
            "lupa:geospatial_entity",
            kwargs={
                'lat': '-22.000',
                'lon': '-43.000',
                'value': 'house'
            }
        )

        response = self.client.get(url).json()

        self.assertEqual(response['abreviation'], 'BAI')
        self.assertEqual(response['entity_id'], 'minhacasa')
        _egsp.assert_called()

    @mock.patch('lupa.views.execute_geospatial', return_value=[])
    def test_empty_geospatial_response(self, _egsp):
        make(
            'lupa.Entidade',
            abreviation='MUN',
            geojson_column="geojson_column",
            osm_value_attached="municipality",
            osm_default_level=False
        )
        make(
            'lupa.Entidade',
            abreviation='BAI',
            geojson_column="geojson_column",
            osm_value_attached="suburb",
            osm_default_level=True
        )

        url = reverse(
            "lupa:geospatial_entity",
            kwargs={
                'lat': '-22.000',
                'lon': '-43.000',
                'value': 'house'
            }
        )

        response = self.client.get(url)

        self.assertEqual(response.status_code, 404)
        _egsp.assert_called()

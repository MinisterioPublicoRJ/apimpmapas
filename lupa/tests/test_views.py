from unittest import mock

from decouple import config
from django.conf import settings
from django.core.cache import cache
from django.test import TestCase
from django.urls import reverse
import jwt
import pytest
from model_bakery.baker import make
import responses
from rest_framework.response import Response

from lupa import osmapi
from lupa.cache import (
    ENTITY_KEY_PREFIX,
    ENTITY_KEY_CHECK,
    DATA_ENTITY_KEY_PREFIX,
    DATA_ENTITY_KEY_CHECK,
    DATA_DETAIL_KEY_PREFIX,
    DATA_DETAIL_KEY_CHECK
)
from lupa.exceptions import QueryError
from .fixtures.osmapi import default_response


class NoCacheTestCase:
    def teardown_method(self, method):
        cache.clear()


class EntidadeViewTest(NoCacheTestCase, TestCase):

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

        make(
            'lupa.DadoEntidade',
            id=1,
            entity_type=estado,
            theme=seguranca,
            order=2
        )
        make(
            'lupa.DadoEntidade',
            id=2,
            entity_type=estado,
            theme=None,
            order=5
        )
        make(
            'lupa.DadoEntidade',
            id=3,
            entity_type=municipio,
            order=7
        )
        make(
            'lupa.DadoEntidade',
            id=4,
            entity_type=estado,
            theme=None,
            order=1
        )
        make(
            'lupa.DadoEntidade',
            id=5,
            entity_type=estado,
            theme=saude,
            order=8
        )
        make(
            'lupa.DadoEntidade',
            id=6,
            entity_type=municipio,
            order=6
        )
        make(
            'lupa.DadoEntidade',
            id=7,
            entity_type=estado,
            theme=seguranca,
            order=3
        )
        make(
            'lupa.DadoEntidade',
            id=8,
            entity_type=estado,
            theme=None,
            order=4
        )

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

    @mock.patch('lupa.views.get_cache')
    @mock.patch('lupa.views.get_object_or_404')
    def test_get_cache_entidade(self, _get_object_or_404, _get_cache):
        expected_response = {'id': 1, 'abreviation': 'EST'}

        _get_object_or_404.return_value = 'mock'
        _get_cache.return_value = Response(expected_response)
        kwargs = {'entity_type': 'EST', 'domain_id': '33'}

        url = reverse('lupa:detail_entidade', args=('EST', '33'))
        resp = self.client.get(url)
        resp_json = resp.json()

        self.assertEqual(resp.status_code, 200)
        call_args = _get_cache.call_args_list[0][0]
        self.assertEqual(
            call_args,
            (ENTITY_KEY_PREFIX, kwargs)
        )
        self.assertEqual(resp_json, expected_response)

    @mock.patch('lupa.views.save_cache')
    @mock.patch('lupa.serializers.execute')
    def test_save_cache_entidade(self, _execute, _save_cache):
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

        make(
            'lupa.DadoEntidade',
            id=1,
            entity_type=estado,
            theme=seguranca,
            order=2
        )
        make(
            'lupa.DadoEntidade',
            id=2,
            entity_type=estado,
            theme=None,
            order=5
        )
        make(
            'lupa.DadoEntidade',
            id=3,
            entity_type=municipio,
            order=7
        )
        make(
            'lupa.DadoEntidade',
            id=4,
            entity_type=estado,
            theme=None,
            order=1
        )
        make(
            'lupa.DadoEntidade',
            id=5,
            entity_type=estado,
            theme=saude,
            order=8
        )
        make(
            'lupa.DadoEntidade',
            id=6,
            entity_type=municipio,
            order=6
        )
        make(
            'lupa.DadoEntidade',
            id=7,
            entity_type=estado,
            theme=seguranca,
            order=3
        )
        make(
            'lupa.DadoEntidade',
            id=8,
            entity_type=estado,
            theme=None,
            order=4
        )

        url = reverse('lupa:detail_entidade', args=('EST', '33',))
        resp = self.client.get(url)

        self.assertEqual(resp.status_code, 200)
        call_args = _save_cache.call_args_list[0][0]
        self.assertEqual(
            call_args,
            (
                expected_answer,
                ENTITY_KEY_PREFIX,
                ENTITY_KEY_CHECK,
                {'entity_type': 'EST', 'domain_id': '33'}
            )
        )


class AuthEntidadeViewTest(NoCacheTestCase, TestCase):

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
        self.assertEqual(resp.status_code, 404)

    def test_entidade_permission_failed(self):
        payload = {'permissions': [self.role_forbidden]}
        token = jwt.encode(payload, config('SECRET_KEY'), algorithm="HS256")

        url = reverse(
            'lupa:detail_entidade',
            args=(self.entity_abrv, self.entity_id)
        )
        resp = self.client.get(url, {'auth_token': token})
        self.assertEqual(resp.status_code, 404)


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

        make('lupa.DadoEntidade', entity_type=ent_estado, _quantity=2)
        dado_object_mun_0 = make(
            'lupa.DadoEntidade',
            entity_type=ent_municipio,
            theme=None,
            order=1
        )
        dado_object_mun_1 = make(
            'lupa.DadoEntidade',
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
            'lupa.DadoEntidade',
            entity_type=ent_municipio,
            show_box=False
        )
        dado_object_mun_1 = make(
            'lupa.DadoEntidade',
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
        self.detail_data_1_id = 23
        self.detail_data_2_id = 59
        self.detail_data_3_id = 102
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
            'icon': settings.MEDIA_URL + self.icon_file,
            'detalhe': [
                {'id': self.detail_data_2_id},
                {'id': self.detail_data_1_id},
                {'id': self.detail_data_3_id},
            ]
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
            'lupa.DadoEntidade',
            id=self.data_id,
            data_type=self.data_type_obj,
            entity_type=entidade,
            exibition_field=self.exibition_field,
            icon__file_path=self.icon_file
        )
        make('lupa.ColunaDado', info_type='id', name='identi', dado=dado)
        make('lupa.ColunaDado', info_type='fonte', name='fon', dado=dado)
        make('lupa.ColunaDado', info_type='dado', name='data', dado=dado)
        make(
            'lupa.DadoDetalhe',
            id=self.detail_data_1_id,
            order=1,
            dado_main=dado
        )
        make(
            'lupa.DadoDetalhe',
            id=self.detail_data_2_id,
            order=0,
            dado_main=dado
        )
        make(
            'lupa.DadoDetalhe',
            id=self.detail_data_3_id,
            order=2,
            dado_main=dado
        )

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
            'lupa.DadoEntidade',
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
            'lupa.DadoEntidade',
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
            'lupa.DadoEntidade',
            id=self.data_id,
            entity_type=entidade
        )

        url = reverse(
            'lupa:detail_dado',
            args=(self.entity_abrv, self.domain_id, self.data_id)
        )
        resp = self.client.get(url)

        self.assertEqual(resp.status_code, 404)

    @mock.patch('lupa.views.get_cache')
    @mock.patch('lupa.views.get_object_or_404')
    def test_dado_get_cache(self, _get_object_or_404, _get_cache):
        expected_response = {
            'id': self.data_id,
            'external_data': {
                'dado': self.external_data,
                'fonte': self.external_source,
                'id': self.data_id
            },
            'exibition_field': self.exibition_field,
            'data_type': self.data_type,
            'icon': settings.MEDIA_URL + self.icon_file,
            'detalhe': [
                {'id': self.detail_data_2_id},
                {'id': self.detail_data_1_id},
                {'id': self.detail_data_3_id},
            ]
        }

        _get_object_or_404.return_value = 'mock'
        _get_cache.return_value = Response(expected_response)
        kwargs = {
            'entity_type': self.entity_abrv,
            'domain_id': self.domain_id,
            'pk': self.data_id
        }

        url = reverse(
            'lupa:detail_dado',
            args=(self.entity_abrv, self.domain_id, self.data_id)
        )
        resp = self.client.get(url)
        resp_json = resp.json()

        self.assertEqual(resp.status_code, 200)
        call_args = _get_cache.call_args_list[0][0]
        self.assertEqual(
            call_args,
            (DATA_ENTITY_KEY_PREFIX, kwargs)
        )
        self.assertEqual(resp_json, expected_response)

    @mock.patch('lupa.views.save_cache')
    @mock.patch('lupa.serializers.execute')
    def test_dado_save_cache(self, _execute, _save_cache):
        expected_response = {
            'id': self.data_id,
            'exibition_field': self.exibition_field,
            'external_data': {
                'dado': self.external_data,
                'fonte': self.external_source,
                'id': self.data_id
            },
            'data_type': self.data_type,
            'icon': None,
            'detalhe': []
        }

        _execute.return_value = [(
            self.external_data,
            self.external_source,
            self.data_id
        )]

        kwargs = {
            'entity_type': self.entity_abrv,
            'domain_id': self.domain_id,
            'pk': self.data_id
        }

        entidade = make(
            'lupa.Entidade',
            id=self.entity_id,
            abreviation=self.entity_abrv,
        )
        dado = make(
            'lupa.DadoEntidade',
            id=self.data_id,
            data_type=self.data_type_obj,
            entity_type=entidade,
            exibition_field=self.exibition_field,
            is_cacheable=True
        )
        make('lupa.ColunaDado', info_type='id', name='identi', dado=dado)
        make('lupa.ColunaDado', info_type='fonte', name='fon', dado=dado)
        make('lupa.ColunaDado', info_type='dado', name='data', dado=dado)

        url = reverse(
            'lupa:detail_dado',
            args=(self.entity_abrv, self.domain_id, self.data_id)
        )
        resp = self.client.get(url)

        self.assertEqual(resp.status_code, 200)
        call_args = _save_cache.call_args_list[0][0]
        self.assertEqual(
            call_args,
            (
                expected_response,
                DATA_ENTITY_KEY_PREFIX,
                DATA_ENTITY_KEY_CHECK,
                kwargs
            )
        )


class AuthDadosViewTest(NoCacheTestCase, TestCase):

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
            'lupa.DadoEntidade',
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
            'detalhe': [],
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
        self.assertEqual(resp.status_code, 404)

    def test_dado_permission_failed(self):
        payload = {'permissions': [self.role_forbidden]}
        token = jwt.encode(payload, config('SECRET_KEY'), algorithm="HS256")

        url = reverse(
            'lupa:detail_dado',
            args=(self.entity_abrv, self.entity_id, self.data_id)
        )
        resp = self.client.get(url, {'auth_token': token})
        self.assertEqual(resp.status_code, 404)


class DetalhesViewTest(TestCase, NoCacheTestCase):
    def setUp(self):
        self.entity_id = 1
        self.entity_abrv = 'EST'
        self.data_id = 7
        self.detail_id = 23
        self.external_data = '202'
        self.exibition_field = 'Abrigos para crianças e adolescentes'
        self.domain_id = '33'
        self.data_type = 'texto_pequeno_destaque'
        self.data_type_obj = make(
            'lupa.TipoDado',
            name=self.data_type,
            serialization='Singleton'
        )

    @mock.patch('lupa.serializers.execute')
    def test_detalhe_ok(self, _execute):

        expected_response = {
            'id': self.detail_id,
            'external_data': {
                'dado': self.external_data,
                'id': self.data_id
            },
            'exibition_field': self.exibition_field,
            'data_type': self.data_type,
        }

        _execute.return_value = [(
            self.external_data,
            self.data_id
        )]

        entidade = make(
            'lupa.Entidade',
            id=self.entity_id,
            abreviation=self.entity_abrv,
        )
        dado = make(
            'lupa.DadoEntidade',
            id=self.data_id,
            entity_type=entidade,
        )
        detalhe = make(
            'lupa.DadoDetalhe',
            id=self.detail_id,
            exibition_field=self.exibition_field,
            dado_main=dado,
            data_type=self.data_type_obj
        )
        make('lupa.ColunaDetalhe', info_type='id', name='identi', dado=detalhe)
        make('lupa.ColunaDetalhe', info_type='dado', name='data', dado=detalhe)

        url = reverse(
            'lupa:detail_detalhes',
            args=(self.entity_abrv, self.domain_id, self.detail_id)
        )
        resp = self.client.get(url)
        resp_json = resp.json()

        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp_json, expected_response)

    @mock.patch('lupa.serializers.execute')
    def test_detalhe_sem_retorno_db(self, _execute):
        _execute.return_value = []

        entidade = make(
            'lupa.Entidade',
            id=self.entity_id,
            abreviation=self.entity_abrv,
        )

        dado = make(
            'lupa.DadoEntidade',
            id=self.data_id,
            entity_type=entidade,
        )

        make(
            'lupa.DadoDetalhe',
            id=self.detail_id,
            dado_main=dado,
            data_type=self.data_type_obj
        )

        url = reverse(
            'lupa:detail_detalhes',
            args=(self.entity_abrv, self.domain_id, self.detail_id)
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
        dado = make(
            'lupa.DadoEntidade',
            id=self.data_id,
            entity_type=entidade
        )
        make(
            'lupa.DadoDetalhe',
            id=self.detail_id,
            dado_main=dado
        )
        url = reverse(
            'lupa:detail_detalhes',
            args=(self.entity_abrv, self.domain_id, self.detail_id)
        )
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 404)

    @mock.patch('lupa.views.get_cache')
    @mock.patch('lupa.views.get_object_or_404')
    def test_detalhe_get_cache(self, _get_object_or_404, _get_cache):
        expected_response = {
            'id': self.detail_id,
            'external_data': {
                'dado': self.external_data,
                'id': self.data_id
            },
            'exibition_field': self.exibition_field,
            'data_type': self.data_type,
        }

        _get_object_or_404.return_value = 'mock'
        _get_cache.return_value = Response(expected_response)
        kwargs = {
            'entity_type': self.entity_abrv,
            'domain_id': self.domain_id,
            'pk': self.detail_id
        }

        url = reverse(
            'lupa:detail_detalhes',
            args=(self.entity_abrv, self.domain_id, self.detail_id)
        )
        resp = self.client.get(url)
        resp_json = resp.json()

        self.assertEqual(resp.status_code, 200)
        call_args = _get_cache.call_args_list[0][0]
        self.assertEqual(
            call_args,
            (DATA_DETAIL_KEY_PREFIX, kwargs)
        )
        self.assertEqual(resp_json, expected_response)

    @mock.patch('lupa.views.save_cache')
    @mock.patch('lupa.serializers.execute')
    def test_detalhe_save_cache(self, _execute, _save_cache):
        expected_response = {
            'id': self.detail_id,
            'external_data': {
                'dado': self.external_data,
                'id': self.data_id
            },
            'exibition_field': self.exibition_field,
            'data_type': self.data_type,
        }

        _execute.return_value = [(
            self.external_data,
            self.data_id
        )]

        kwargs = {
            'entity_type': self.entity_abrv,
            'domain_id': self.domain_id,
            'pk': self.detail_id
        }

        entidade = make(
            'lupa.Entidade',
            id=self.entity_id,
            abreviation=self.entity_abrv,
        )
        dado = make(
            'lupa.DadoEntidade',
            id=self.data_id,
            entity_type=entidade,
        )
        detalhe = make(
            'lupa.DadoDetalhe',
            id=self.detail_id,
            exibition_field=self.exibition_field,
            dado_main=dado,
            data_type=self.data_type_obj,
            is_cacheable=True
        )
        make('lupa.ColunaDetalhe', info_type='id', name='identi', dado=detalhe)
        make('lupa.ColunaDetalhe', info_type='dado', name='data', dado=detalhe)

        url = reverse(
            'lupa:detail_detalhes',
            args=(self.entity_abrv, self.domain_id, self.detail_id)
        )
        resp = self.client.get(url)

        self.assertEqual(resp.status_code, 200)
        call_args = _save_cache.call_args_list[0][0]
        self.assertEqual(
            call_args,
            (
                expected_response,
                DATA_DETAIL_KEY_PREFIX,
                DATA_DETAIL_KEY_CHECK,
                kwargs
            )
        )


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

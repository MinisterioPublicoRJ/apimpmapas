import datetime as dt
from unittest import mock

import pytest
from django.test import TestCase
from freezegun import freeze_time
from model_bakery.baker import make
from rest_framework.response import Response

from lupa.cache import (
    cache_key,
    wildcard_cache_key,
    _repopulate_cache_data_entity,
    _repopulate_cache_data_detail,
    _repopulate_cache_entity,
    _remove_from_cache,
    wrap_response,
    repopulate_cache,
    get_cache,
    _has_role
)
from lupa.models import Entidade, DadoEntidade, DadoDetalhe


class Cache(TestCase):
    def test_create_querystring_entidade(self):
        kwargs = {'entity_type': 'EST', 'domain_id': '33'}
        key_prefix = 'key_prefix'

        key = cache_key(key_prefix, kwargs)
        expected_key = 'key_prefix:EST:33'

        self.assertEqual(key, expected_key)

    def test_create_querystring_dados(self):
        kwargs = {'entity_type': 'MUN', 'domain_id': '33600', 'pk': '71'}
        key_prefix = 'key_prefix'

        key = cache_key(key_prefix, kwargs)
        expected_key = 'key_prefix:MUN:33600:71'

        self.assertEqual(key, expected_key)

    def test_create_cache_key_for_entity_removal(self):
        keys = ['MUN']
        key_prefix = 'prefix'

        key = wildcard_cache_key(key_prefix, keys)
        expected_key = '*prefix:MUN:*'

        self.assertEqual(key, expected_key)

    def test_create_cache_key_for_data_removal(self):
        keys = ['MUN', '71']
        key_prefix = 'prefix'

        key = wildcard_cache_key(key_prefix, keys)
        expected_key = '*prefix:MUN:*:71'

        self.assertEqual(key, expected_key)

    def test_wrap_response_with_data_and_status_code_200(self):
        key_check = 'check'
        response_data = {'some_response': 'response', 'check': 'check_data'}

        wrapped_resp = wrap_response(response_data, key_check)
        expected_response = {
            'data': response_data,
            'status_code': 200
        }

        self.assertEqual(wrapped_resp, expected_response)

    def test_wrap_response_with_data_and_status_code_404(self):
        key_check = 'check'
        response_data = {'some_other_data': 'data'}

        wrapped_resp = wrap_response(response_data, key_check)
        expected_response = {
            'data': {"detail": "Não encontrado."},
            'status_code': 404
        }

        self.assertEqual(wrapped_resp, expected_response)

    @mock.patch('lupa.cache.cache_key')
    @mock.patch('lupa.cache.django_cache')
    def test_get_cache(self, _django_cache, _cache_key):
        key_data = 'key'
        cache_data = 'cache_data'
        request_args = {'arg': 'arg_data'}
        prefix = 'prefix'
        expected_response = Response(cache_data, status=200)

        _django_cache.__contains__.return_value = True
        _django_cache.get.return_value = {
            'data': cache_data,
            'status_code': 200
        }
        _cache_key.return_value = key_data

        cache = get_cache(prefix, request_args)

        _django_cache.get.assert_called_once_with(key_data)
        self.assertEqual(200, expected_response.status_code)
        self.assertEqual(cache.data, expected_response.data)

    def test_check_has_roles(self):
        grupo = make('lupa.Grupo', role='ROLE_OK')
        obj = make('lupa.Entidade', roles_allowed=[grupo])
        permissions = ['ROLE_OK']
        has_roles = _has_role(obj, permissions)

        self.assertTrue(has_roles)

    def test_check_hasnt_roles(self):
        grupo = make('lupa.Grupo', role='ROLE_OK')
        obj = make('lupa.Entidade', roles_allowed=[grupo])
        permissions = ['ROLE_NOT_OK']
        has_roles = _has_role(obj, permissions)

        self.assertFalse(has_roles)

    def test_check_has_default(self):
        obj = make('lupa.Entidade')
        permissions = []
        has_roles = _has_role(obj, permissions)
        self.assertTrue(has_roles)


@pytest.mark.django_db(transaction=True)
class ModelCache(TestCase):
    def setUp(self):
        self.role_allowed = 'role_allowed'
        self.entity_abrv = 'EST'
        self.entity_type = 'Estado'
        self.entity_name = 'Rio de Janeiro'

        municipio = make('lupa.Entidade', abreviation='MUN')
        self.grupo_allowed = make(
            'lupa.Grupo',
            role=self.role_allowed
        )
        estado = make(
            'lupa.Entidade',
            roles_allowed=[self.grupo_allowed],
            name=self.entity_type,
            abreviation=self.entity_abrv
        )
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
        self.expected_answer = {
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
        self.estado = estado


@pytest.mark.django_db(transaction=True)
class RepopulateCache(TestCase):
    @freeze_time('2019-10-29')
    @mock.patch('lupa.serializers.execute')
    @mock.patch('lupa.cache.execute_sample')
    @mock.patch('lupa.cache.cache_key')
    @mock.patch('lupa.cache.django_cache')
    def test_repopulate_cache_with_lupa_dados_entidade(
            self,
            _django_cache,
            _cache_key,
            _execute_sample,
            _execute):

        _execute.return_value = [(
            '202',
            7
        )]
        _execute_sample.side_effect = (
            [('33001',), ('33002',), ('33003',), ('33004',)],
            [('33010',), ('33011',), ('33012',), ('33013',)],
        )
        _cache_key.side_effect = ['key %s' % k for k in range(1, 17)]
        municipio = make('lupa.Entidade', abreviation='MUN')
        estado = make(
            'lupa.Entidade',
            abreviation='EST'
        )

        dado_1 = make(
            'lupa.DadoEntidade',
            pk=1,
            entity_type=estado,
            order=2,
            cache_timeout_days=10
        )
        dado_2 = make(
            'lupa.DadoEntidade',
            pk=2,
            entity_type=municipio,
            order=7,
            cache_timeout_days=20
        )
        dado_3 = make(
            'lupa.DadoEntidade',
            pk=3,
            entity_type=estado,
            order=1,
            cache_timeout_days=30
        )
        dado_4 = make(
            'lupa.DadoEntidade',
            pk=4,
            entity_type=municipio,
            order=6,
            cache_timeout_days=40
        )
        make('lupa.ColunaDado', info_type='id', name='identi', dado=dado_1)
        make('lupa.ColunaDado', info_type='id', name='identi', dado=dado_2)
        make('lupa.ColunaDado', info_type='id', name='identi', dado=dado_3)
        make('lupa.ColunaDado', info_type='id', name='identi', dado=dado_4)

        queryset = DadoEntidade.objects.all()
        _repopulate_cache_data_entity(
            key_prefix='lupa_dado_entidade',
            queryset=queryset,
        )

        execute_sample_calls = [
            mock.call(
                estado.database,
                estado.schema,
                estado.table,
                [estado.id_column],
                limit=False
            ),
            mock.call(
                municipio.database,
                municipio.schema,
                municipio.table,
                [municipio.id_column],
                limit=False
            )

        ]

        cache_key_calls = [
            mock.call('lupa_dado_entidade',
                      {'entity_type': dado_3.entity_type.abreviation,
                       'domain_id': '33001',
                       'pk': 3
                       }
                      ),
            mock.call('lupa_dado_entidade',
                      {'entity_type': dado_3.entity_type.abreviation,
                       'domain_id': '33002',
                       'pk': 3
                       }
                      ),
            mock.call('lupa_dado_entidade',
                      {'entity_type': dado_3.entity_type.abreviation,
                       'domain_id': '33003',
                       'pk': 3
                       }
                      ),
            mock.call('lupa_dado_entidade',
                      {'entity_type': dado_3.entity_type.abreviation,
                       'domain_id': '33004',
                       'pk': 3
                       }
                      ),
            mock.call('lupa_dado_entidade',
                      {'entity_type': dado_1.entity_type.abreviation,
                       'domain_id': '33001',
                       'pk': 1
                       }
                      ),
            mock.call('lupa_dado_entidade',
                      {'entity_type': dado_1.entity_type.abreviation,
                       'domain_id': '33002',
                       'pk': 1
                       }
                      ),
            mock.call('lupa_dado_entidade',
                      {'entity_type': dado_1.entity_type.abreviation,
                       'domain_id': '33003',
                       'pk': 1
                       }
                      ),
            mock.call('lupa_dado_entidade',
                      {'entity_type': dado_1.entity_type.abreviation,
                       'domain_id': '33004',
                       'pk': 1
                       }
                      ),
            mock.call('lupa_dado_entidade',
                      {'entity_type': dado_4.entity_type.abreviation,
                       'domain_id': '33010',
                       'pk': 4
                       }
                      ),
            mock.call('lupa_dado_entidade',
                      {'entity_type': dado_4.entity_type.abreviation,
                       'domain_id': '33011',
                       'pk': 4
                       }
                      ),
            mock.call('lupa_dado_entidade',
                      {'entity_type': dado_4.entity_type.abreviation,
                       'domain_id': '33012',
                       'pk': 4
                       }
                      ),
            mock.call('lupa_dado_entidade',
                      {'entity_type': dado_4.entity_type.abreviation,
                       'domain_id': '33013',
                       'pk': 4
                       }
                      ),
            mock.call('lupa_dado_entidade',
                      {'entity_type': dado_2.entity_type.abreviation,
                       'domain_id': '33010',
                       'pk': 2
                       }
                      ),
            mock.call('lupa_dado_entidade',
                      {'entity_type': dado_2.entity_type.abreviation,
                       'domain_id': '33011',
                       'pk': 2
                       }
                      ),
            mock.call('lupa_dado_entidade',
                      {'entity_type': dado_2.entity_type.abreviation,
                       'domain_id': '33012',
                       'pk': 2
                       }
                      ),
            mock.call('lupa_dado_entidade',
                      {'entity_type': dado_2.entity_type.abreviation,
                       'domain_id': '33013',
                       'pk': 2
                       }
                      ),
        ]
        _django_cache_calls = [
            mock.call('key 1', {'data': {'id': dado_3.pk,
                                         'exibition_field': None,
                                         'external_data': {'id': '202'},
                                         'data_type': dado_3.data_type.name,
                                         'icon': None,
                                         'detalhe': []},
                                'status_code': 200},
                      timeout=dado_3.cache_timeout_sec
                      ),
            mock.call('key 2', {'data': {'id': dado_3.pk,
                                         'exibition_field': None,
                                         'external_data': {'id': '202'},
                                         'data_type': dado_3.data_type.name,
                                         'icon': None,
                                         'detalhe': []},
                                'status_code': 200},
                      timeout=dado_3.cache_timeout_sec
                      ),
            mock.call('key 3', {'data': {'id': dado_3.pk,
                                         'exibition_field': None,
                                         'external_data': {'id': '202'},
                                         'data_type': dado_3.data_type.name,
                                         'icon': None,
                                         'detalhe': []},
                                'status_code': 200},
                      timeout=dado_3.cache_timeout_sec
                      ),
            mock.call('key 4', {'data': {'id': dado_3.pk,
                                         'exibition_field': None,
                                         'external_data': {'id': '202'},
                                         'data_type': dado_3.data_type.name,
                                         'icon': None,
                                         'detalhe': []},
                                'status_code': 200},
                      timeout=dado_3.cache_timeout_sec
                      ),
            mock.call('key 5', {'data': {'id': dado_1.pk,
                                         'exibition_field': None,
                                         'external_data': {'id': '202'},
                                         'data_type': dado_1.data_type.name,
                                         'icon': None,
                                         'detalhe': []},
                                'status_code': 200},
                      timeout=dado_1.cache_timeout_sec
                      ),
            mock.call('key 6', {'data': {'id': dado_1.pk,
                                         'exibition_field': None,
                                         'external_data': {'id': '202'},
                                         'data_type': dado_1.data_type.name,
                                         'icon': None,
                                         'detalhe': []},
                                'status_code': 200},
                      timeout=dado_1.cache_timeout_sec
                      ),
            mock.call('key 7', {'data': {'id': dado_1.pk,
                                         'exibition_field': None,
                                         'external_data': {'id': '202'},
                                         'data_type': dado_1.data_type.name,
                                         'icon': None,
                                         'detalhe': []},
                                'status_code': 200},
                      timeout=dado_1.cache_timeout_sec
                      ),
            mock.call('key 8', {'data': {'id': dado_1.pk,
                                         'exibition_field': None,
                                         'external_data': {'id': '202'},
                                         'data_type': dado_1.data_type.name,
                                         'icon': None,
                                         'detalhe': []},
                                'status_code': 200},
                      timeout=dado_1.cache_timeout_sec
                      ),
            mock.call('key 9', {'data': {'id': dado_4.pk,
                                         'exibition_field': None,
                                         'external_data': {'id': '202'},
                                         'data_type': dado_4.data_type.name,
                                         'icon': None,
                                         'detalhe': []},
                                'status_code': 200},
                      timeout=dado_4.cache_timeout_sec
                      ),
            mock.call('key 10', {'data': {'id': dado_4.pk,
                                          'exibition_field': None,
                                          'external_data': {'id': '202'},
                                          'data_type': dado_4.data_type.name,
                                          'icon': None,
                                          'detalhe': []},
                                 'status_code': 200},
                      timeout=dado_4.cache_timeout_sec
                      ),
            mock.call('key 11', {'data': {'id': dado_4.pk,
                                          'exibition_field': None,
                                          'external_data': {'id': '202'},
                                          'data_type': dado_4.data_type.name,
                                          'icon': None,
                                          'detalhe': []},
                                 'status_code': 200},
                      timeout=dado_4.cache_timeout_sec
                      ),
            mock.call('key 12', {'data': {'id': dado_4.pk,
                                          'exibition_field': None,
                                          'external_data': {'id': '202'},
                                          'data_type': dado_4.data_type.name,
                                          'icon': None,
                                          'detalhe': []},
                                 'status_code': 200},
                      timeout=dado_4.cache_timeout_sec
                      ),
            mock.call('key 13', {'data': {'id': dado_2.pk,
                                          'exibition_field': None,
                                          'external_data': {'id': '202'},
                                          'data_type': dado_2.data_type.name,
                                          'icon': None,
                                          'detalhe': []},
                                 'status_code': 200},
                      timeout=dado_2.cache_timeout_sec
                      ),
            mock.call('key 14', {'data': {'id': dado_2.pk,
                                          'exibition_field': None,
                                          'external_data': {'id': '202'},
                                          'data_type': dado_2.data_type.name,
                                          'icon': None,
                                          'detalhe': []},
                                 'status_code': 200},
                      timeout=dado_2.cache_timeout_sec
                      ),
            mock.call('key 15', {'data': {'id': dado_2.pk,
                                          'exibition_field': None,
                                          'external_data': {'id': '202'},
                                          'data_type': dado_2.data_type.name,
                                          'icon': None,
                                          'detalhe': []},
                                 'status_code': 200},
                      timeout=dado_2.cache_timeout_sec
                      ),
            mock.call('key 16', {'data': {'id': dado_2.pk,
                                          'exibition_field': None,
                                          'external_data': {'id': '202'},
                                          'data_type': dado_2.data_type.name,
                                          'icon': None,
                                          'detalhe': []},
                                 'status_code': 200},
                      timeout=dado_2.cache_timeout_sec
                      ),
        ]
        updated_dado_entidade = DadoEntidade.objects.all()
        expected_dt = dt.date.today()

        _execute_sample.assert_has_calls(execute_sample_calls)
        _cache_key.assert_has_calls(cache_key_calls)
        _django_cache.set.assert_has_calls(_django_cache_calls)
        self.assertTrue(
            all([d.last_cache_update == expected_dt
                 for d in updated_dado_entidade]
                )
        )

    @mock.patch('lupa.serializers.execute')
    @mock.patch('lupa.cache.execute_sample')
    @mock.patch('lupa.cache.cache_key')
    @mock.patch('lupa.cache.django_cache')
    def test_repopulate_cache_with_lupa_dados_detalhe(
            self,
            _django_cache,
            _cache_key,
            _execute_sample,
            _execute):

        _execute.return_value = [(
            '202',
            7
        )]
        _execute_sample.side_effect = (
            [('33001',), ('33002',), ('33003',), ('33004',)],
            [('33010',), ('33011',), ('33012',), ('33013',)],
        )
        _cache_key.side_effect = ['key %s' % k for k in range(1, 17)]
        municipio = make('lupa.Entidade', abreviation='MUN')
        estado = make('lupa.Entidade', abreviation='EST')

        dado_entidade_estado = make(
            'lupa.DadoEntidade',
            pk=1,
            entity_type=estado,
            cache_timeout_days=10,
        )
        dado_entidade_municipio = make(
            'lupa.DadoEntidade',
            pk=2,
            entity_type=municipio,
            cache_timeout_days=10,
        )
        dado_1 = make(
            'lupa.DadoDetalhe',
            pk=1,
            dado_main=dado_entidade_estado,
            order=7,
            cache_timeout_days=20,
        )
        dado_2 = make(
            'lupa.DadoDetalhe',
            pk=2,
            dado_main=dado_entidade_municipio,
            order=7,
            cache_timeout_days=20
        )
        dado_3 = make(
            'lupa.DadoDetalhe',
            pk=3,
            dado_main=dado_entidade_estado,
            order=1,
            cache_timeout_days=30
        )
        dado_4 = make(
            'lupa.DadoDetalhe',
            pk=4,
            dado_main=dado_entidade_municipio,
            order=6,
            cache_timeout_days=40
        )
        make('lupa.ColunaDetalhe', info_type='id', name='identi', dado=dado_1)
        make('lupa.ColunaDetalhe', info_type='id', name='identi', dado=dado_2)
        make('lupa.ColunaDetalhe', info_type='id', name='identi', dado=dado_3)
        make('lupa.ColunaDetalhe', info_type='id', name='identi', dado=dado_4)

        queryset = DadoDetalhe.objects.all()
        _repopulate_cache_data_detail(
            key_prefix='lupa_dado_detalhe',
            queryset=queryset,
        )

        execute_sample_calls = [
            mock.call(
                estado.database,
                estado.schema,
                estado.table,
                [estado.id_column],
                limit=False
            ),
            mock.call(
                municipio.database,
                municipio.schema,
                municipio.table,
                [municipio.id_column],
                limit=False
            )

        ]

        cache_key_calls = [
            mock.call('lupa_dado_detalhe',
                      {'entity_type': dado_3.dado_main.entity_type.abreviation,
                       'domain_id': '33001',
                       'pk': 3
                       }
                      ),
            mock.call('lupa_dado_detalhe',
                      {'entity_type': dado_3.dado_main.entity_type.abreviation,
                       'domain_id': '33002',
                       'pk': 3
                       }
                      ),
            mock.call('lupa_dado_detalhe',
                      {'entity_type': dado_3.dado_main.entity_type.abreviation,
                       'domain_id': '33003',
                       'pk': 3
                       }
                      ),
            mock.call('lupa_dado_detalhe',
                      {'entity_type': dado_3.dado_main.entity_type.abreviation,
                       'domain_id': '33004',
                       'pk': 3
                       }
                      ),
            mock.call('lupa_dado_detalhe',
                      {'entity_type': dado_1.dado_main.entity_type.abreviation,
                       'domain_id': '33001',
                       'pk': 1
                       }
                      ),
            mock.call('lupa_dado_detalhe',
                      {'entity_type': dado_1.dado_main.entity_type.abreviation,
                       'domain_id': '33002',
                       'pk': 1
                       }
                      ),
            mock.call('lupa_dado_detalhe',
                      {'entity_type': dado_1.dado_main.entity_type.abreviation,
                       'domain_id': '33003',
                       'pk': 1
                       }
                      ),
            mock.call('lupa_dado_detalhe',
                      {'entity_type': dado_1.dado_main.entity_type.abreviation,
                       'domain_id': '33004',
                       'pk': 1
                       }
                      ),
            mock.call('lupa_dado_detalhe',
                      {'entity_type': dado_4.dado_main.entity_type.abreviation,
                       'domain_id': '33010',
                       'pk': 4
                       }
                      ),
            mock.call('lupa_dado_detalhe',
                      {'entity_type': dado_4.dado_main.entity_type.abreviation,
                       'domain_id': '33011',
                       'pk': 4
                       }
                      ),
            mock.call('lupa_dado_detalhe',
                      {'entity_type': dado_4.dado_main.entity_type.abreviation,
                       'domain_id': '33012',
                       'pk': 4
                       }
                      ),
            mock.call('lupa_dado_detalhe',
                      {'entity_type': dado_4.dado_main.entity_type.abreviation,
                       'domain_id': '33013',
                       'pk': 4
                       }
                      ),
            mock.call('lupa_dado_detalhe',
                      {'entity_type': dado_2.dado_main.entity_type.abreviation,
                       'domain_id': '33010',
                       'pk': 2
                       }
                      ),
            mock.call('lupa_dado_detalhe',
                      {'entity_type': dado_2.dado_main.entity_type.abreviation,
                       'domain_id': '33011',
                       'pk': 2
                       }
                      ),
            mock.call('lupa_dado_detalhe',
                      {'entity_type': dado_2.dado_main.entity_type.abreviation,
                       'domain_id': '33012',
                       'pk': 2
                       }
                      ),
            mock.call('lupa_dado_detalhe',
                      {'entity_type': dado_2.dado_main.entity_type.abreviation,
                       'domain_id': '33013',
                       'pk': 2
                       }
                      ),
        ]
        _django_cache_calls = [
            mock.call('key 1', {'data': {'id': dado_3.pk,
                                         'exibition_field': None,
                                         'external_data': {'id': '202'},
                                         'data_type': dado_3.data_type.name},
                                'status_code': 200},
                      timeout=dado_3.cache_timeout_sec
                      ),
            mock.call('key 2', {'data': {'id': dado_3.pk,
                                         'exibition_field': None,
                                         'external_data': {'id': '202'},
                                         'data_type': dado_3.data_type.name},
                                'status_code': 200},
                      timeout=dado_3.cache_timeout_sec
                      ),
            mock.call('key 3', {'data': {'id': dado_3.pk,
                                         'exibition_field': None,
                                         'external_data': {'id': '202'},
                                         'data_type': dado_3.data_type.name},
                                'status_code': 200},
                      timeout=dado_3.cache_timeout_sec
                      ),
            mock.call('key 4', {'data': {'id': dado_3.pk,
                                         'exibition_field': None,
                                         'external_data': {'id': '202'},
                                         'data_type': dado_3.data_type.name},
                                'status_code': 200},
                      timeout=dado_3.cache_timeout_sec
                      ),
            mock.call('key 5', {'data': {'id': dado_1.pk,
                                         'exibition_field': None,
                                         'external_data': {'id': '202'},
                                         'data_type': dado_1.data_type.name},
                                'status_code': 200},
                      timeout=dado_1.cache_timeout_sec
                      ),
            mock.call('key 6', {'data': {'id': dado_1.pk,
                                         'exibition_field': None,
                                         'external_data': {'id': '202'},
                                         'data_type': dado_1.data_type.name},
                                'status_code': 200},
                      timeout=dado_1.cache_timeout_sec
                      ),
            mock.call('key 7', {'data': {'id': dado_1.pk,
                                         'exibition_field': None,
                                         'external_data': {'id': '202'},
                                         'data_type': dado_1.data_type.name},
                                'status_code': 200},
                      timeout=dado_1.cache_timeout_sec
                      ),
            mock.call('key 8', {'data': {'id': dado_1.pk,
                                         'exibition_field': None,
                                         'external_data': {'id': '202'},
                                         'data_type': dado_1.data_type.name},
                                'status_code': 200},
                      timeout=dado_1.cache_timeout_sec
                      ),
            mock.call('key 9', {'data': {'id': dado_4.pk,
                                         'exibition_field': None,
                                         'external_data': {'id': '202'},
                                         'data_type': dado_4.data_type.name},
                                'status_code': 200},
                      timeout=dado_4.cache_timeout_sec
                      ),
            mock.call('key 10', {'data': {'id': dado_4.pk,
                                          'exibition_field': None,
                                          'external_data': {'id': '202'},
                                          'data_type': dado_4.data_type.name},
                                 'status_code': 200},
                      timeout=dado_4.cache_timeout_sec
                      ),
            mock.call('key 11', {'data': {'id': dado_4.pk,
                                          'exibition_field': None,
                                          'external_data': {'id': '202'},
                                          'data_type': dado_4.data_type.name},
                                 'status_code': 200},
                      timeout=dado_4.cache_timeout_sec
                      ),
            mock.call('key 12', {'data': {'id': dado_4.pk,
                                          'exibition_field': None,
                                          'external_data': {'id': '202'},
                                          'data_type': dado_4.data_type.name},
                                 'status_code': 200},
                      timeout=dado_4.cache_timeout_sec
                      ),
            mock.call('key 13', {'data': {'id': dado_2.pk,
                                          'exibition_field': None,
                                          'external_data': {'id': '202'},
                                          'data_type': dado_2.data_type.name},
                                 'status_code': 200},
                      timeout=dado_2.cache_timeout_sec
                      ),
            mock.call('key 14', {'data': {'id': dado_2.pk,
                                          'exibition_field': None,
                                          'external_data': {'id': '202'},
                                          'data_type': dado_2.data_type.name},
                                 'status_code': 200},
                      timeout=dado_2.cache_timeout_sec
                      ),
            mock.call('key 15', {'data': {'id': dado_2.pk,
                                          'exibition_field': None,
                                          'external_data': {'id': '202'},
                                          'data_type': dado_2.data_type.name},
                                 'status_code': 200},
                      timeout=dado_2.cache_timeout_sec
                      ),
            mock.call('key 16', {'data': {'id': dado_2.pk,
                                          'exibition_field': None,
                                          'external_data': {'id': '202'},
                                          'data_type': dado_2.data_type.name},
                      'status_code': 200},
                      timeout=dado_2.cache_timeout_sec
                      ),
        ]
        updated_dado_detalhe = DadoDetalhe.objects.all()
        expected_dt = dt.date.today()

        _execute_sample.assert_has_calls(execute_sample_calls)
        _cache_key.assert_has_calls(cache_key_calls)
        _django_cache.set.assert_has_calls(_django_cache_calls)
        self.assertTrue(
            all([d.last_cache_update == expected_dt
                 for d in updated_dado_detalhe]
                )
        )

    @mock.patch('lupa.serializers.execute')
    @mock.patch('lupa.cache.execute_sample')
    @mock.patch('lupa.cache.cache_key')
    @mock.patch('lupa.cache.django_cache')
    def test_repopulate_cache_with_lupa_entidades(
            self,
            _django_cache,
            _cache_key,
            _execute_sample,
            _execute):

        _execute.side_effect = [
            [(1, )],
            [(2, )],
        ]
        municipio = make('lupa.Entidade', abreviation='MUN')
        estado = make(
            'lupa.Entidade',
            abreviation='EST'
        )
        _cache_key.side_effect = ['key 1', 'key 2']
        _execute_sample.side_effect = (
            [('33001',)],
            [('33010',)],
        )

        queryset = Entidade.objects.all()

        _repopulate_cache_entity(
            key_prefix='lupa_entidade',
            queryset=queryset,
        )
        execute_sample_calls = [
            mock.call(
                estado.database,
                estado.schema,
                estado.table,
                [estado.id_column],
                limit=False
            ),
            mock.call(
                municipio.database,
                municipio.schema,
                municipio.table,
                [municipio.id_column],
                limit=False
            )

        ]
        django_cache_calls = [
            mock.call('key 1', {'data': {'domain_id': '33001',
                                         'entity_type': estado.name,
                                         'exibition_field': 1,
                                         'geojson': None, 'theme_list': []},
                                'status_code':  200},
                      timeout=estado.cache_timeout_sec
                      ),
            mock.call('key 2', {'data': {'domain_id': '33010',
                                         'entity_type': municipio.name,
                                         'exibition_field': 2,
                                         'geojson': None, 'theme_list': []},
                                'status_code': 200},
                      timeout=municipio.cache_timeout_sec
                      ),
        ]
        cache_key_calls = [
            mock.call('lupa_entidade',
                      {'entity_type': estado.abreviation,
                       'domain_id': '33001',
                       }
                      ),
            mock.call('lupa_entidade',
                      {'entity_type': municipio.abreviation,
                       'domain_id': '33010',
                       }
                      )
        ]
        updated_entidade = Entidade.objects.all()
        expected_dt = dt.date.today()

        _execute_sample.assert_has_calls(execute_sample_calls)
        _cache_key.assert_has_calls(cache_key_calls)
        _django_cache.set.assert_has_calls(django_cache_calls)
        self.assertTrue(
            all([d.last_cache_update == expected_dt
                 for d in updated_entidade]
                )
        )

    @mock.patch('lupa.cache.cache_key')
    @mock.patch('lupa.cache.STDERR')
    @mock.patch('lupa.cache.execute_sample')
    def test_update_cache_serializer_exception(
            self, _execute_sample, _stderr, _cache_key):

        serializer_mock = mock.MagicMock()
        serializer_mock.side_effect = Exception()

        _execute_sample.side_effect = (
            [('33001',)],
        )

        entidade = make(
            'lupa.Entidade',
            last_cache_update=dt.date(2019, 10, 10)
        )

        queryset = Entidade.objects.all()
        entities = queryset.distinct('abreviation').order_by('abreviation')
        repopulate_cache(
            key_prefix='lupa_entidade',
            queryset=queryset,
            entities=entities,
            serializer=serializer_mock,
            key_check='teste'
        )
        expected_msg = 'NOK - %s' % ' - '.join(
            [entidade.database,
             entidade.schema,
             entidade.table,
             entidade.id_column,
             '33001'
             ]
        )

        _stderr.write.assert_called_once_with(expected_msg)
        _cache_key.assert_not_called()


class RemoveFromCache(TestCase):
    @mock.patch('lupa.cache.wildcard_cache_key')
    @mock.patch('lupa.cache.django_cache')
    def test_remove_objs_from_cache(self, _django_cache, _wildcard):
        cache_client_mock = mock.MagicMock()
        cache_client_mock.keys.side_effect = [['KEY 1'], ['KEY 2']]
        _django_cache.get_master_client.return_value = cache_client_mock
        _wildcard.side_effect = ['key 1', 'key 2']
        key_prefix = 'prefix'
        entities = make('lupa.Entidade', _quantity=2)

        _remove_from_cache(key_prefix, ['abreviation'], entities)

        _django_cache.get_master_client.assert_called_once_with()
        wildcard_calls = [
            mock.call(key_prefix, [entities[0].abreviation]),
            mock.call(key_prefix, [entities[1].abreviation])
        ]
        _wildcard.assert_has_calls(wildcard_calls)
        self.assertEqual(
            cache_client_mock.keys.call_args_list[0][0][0],
            'key 1'
        )
        self.assertEqual(
            cache_client_mock.keys.call_args_list[1][0][0],
            'key 2'
        )

        cache_client_mock.delete.assert_has_calls(
            [mock.call('KEY 1'), mock.call('KEY 2')]
        )

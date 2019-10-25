import jwt

from unittest import mock

from decouple import config
from django.test import TestCase
from model_mommy.mommy import make
from rest_framework.response import Response

from lupa.cache import (
    cache_key,
    custom_cache,
    wildcard_cache_key,
    _repopulate_cache_data,
    _repopulate_cache_entity
)
from lupa.models import Entidade, DadoEntidade
from lupa.serializers import EntidadeSerializer, DadoEntidadeSerializer


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


class DecoratorCache(TestCase):
    def setUp(self):
        self.role_allowed = 'role_allowed'
        self.entity_abrv = 'EST'
        self.entity_type = 'Estado'
        self.entity_name = 'Rio de Janeiro'
        self.entity_id = '1'

        municipio = make('lupa.Entidade', abreviation='MUN')
        self.grupo_allowed = make(
            'lupa.Grupo',
            role=self.role_allowed
        )
        estado = make(
            'lupa.Entidade',
            id=self.entity_id,
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
            theme=None, order=1
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

    @mock.patch('lupa.cache.django_cache')
    def test_insert_data_in_cache(self, _django_cache):
        request_mock = mock.MagicMock()
        request_mock.GET = {'auth_token': 'abc1234'}
        class_mock = mock.MagicMock()
        class_mock.queryset = Entidade.objects.all()
        kwargs = {'entity_type': 'MUN', 'domain_id': '1'}

        def mock_view_get(self, request, *args, **kwargs):
            # spec: force mock to be Response class
            response_mock = mock.MagicMock(spec=Response)
            response_mock.data = {'data': '12345'}
            response_mock.status_code = 200
            return response_mock

        decorated_mock_view = custom_cache(
            key_prefix='prefix', model_kwargs={'abreviation': 'entity_type'})(
            mock_view_get
        )

        response = decorated_mock_view(class_mock, request_mock, **kwargs)

        _django_cache.set.assert_called_once_with(
            'prefix:MUN:1', {'data': '12345'},
            timeout=None
        )
        self.assertIsInstance(response, Response)

    @mock.patch('lupa.cache.django_cache')
    def test_retrieve_data_from_cache_with_permission(self, _django_cache):
        _django_cache.__contains__.return_value = True
        _django_cache.get.return_value = {'data': '12345'}
        request_mock = mock.MagicMock()

        payload = {
            'uid': 'username',
            'permissions': 'role_allowed'
        }
        secret = config('SECRET_KEY')
        token = jwt.encode(payload, secret, algorithm="HS256")

        request_mock.GET = {'auth_token': token}

        class_mock = mock.MagicMock()
        class_mock.queryset = Entidade.objects.all()
        kwargs = {'entity_type': 'EST', 'domain_id': '1'}

        def mock_view_get(self, request, *args, **kwargs):
            return None

        decorated_mock_view = custom_cache(
            key_prefix='prefix', model_kwargs={'abreviation': 'entity_type'})(
            mock_view_get
        )

        response = decorated_mock_view(class_mock, request_mock, **kwargs)

        _django_cache.get.assert_called_once_with(
            'prefix:EST:1'
        )
        self.assertIsInstance(response, Response)
        self.assertEqual(response.data, {'data': '12345'})

    @mock.patch('lupa.cache.django_cache')
    def test_donot_retrieve_data_from_cache_wo_permission(self, _django_cache):
        _django_cache.__contains__.return_value = True
        _django_cache.get.return_value = {'data': '12345'}
        request_mock = mock.MagicMock()

        payload = {
            'uid': 'username',
            'permissions': 'role_not_allowed'
        }
        secret = config('SECRET_KEY')
        token = jwt.encode(payload, secret, algorithm="HS256")

        request_mock.GET = {'auth_token': token}

        class_mock = mock.MagicMock()
        class_mock.queryset = Entidade.objects.all()
        kwargs = {'entity_type': 'EST', 'domain_id': '1'}

        def mock_view_get(self, request, *args, **kwargs):
            response_mock = mock.MagicMock(spec=Response)
            response_mock.data = {'data': '12345'}
            response_mock.status_code = 200
            return response_mock

        decorated_mock_view = custom_cache(
            key_prefix='prefix', model_kwargs={'abreviation': 'entity_type'})(
            mock_view_get
        )

        response = decorated_mock_view(class_mock, request_mock, **kwargs)

        _django_cache.get.assert_not_called()
        _django_cache.set.assert_called_once_with(
            'prefix:EST:1', {'data': '12345'},
            timeout=None
        )
        self.assertIsInstance(response, Response)
        self.assertEqual(response.data, {'data': '12345'})

    @mock.patch('lupa.cache.get_object_or_404')
    @mock.patch('lupa.cache.django_cache')
    def test_set_custom_model_fields(self, _django_cache, _get_obj_or_404):
        kwargs = {'entity_type': 'EST', 'domain_id': '1', 'pk': '17'}
        request_mock = mock.MagicMock()

        payload = {
            'uid': 'username',
            'permissions': 'role_not_allowed'
        }
        secret = config('SECRET_KEY')
        token = jwt.encode(payload, secret, algorithm="HS256")

        request_mock.GET = {'auth_token': token}

        class_mock = mock.MagicMock()
        class_mock.queryset = ['queryset']

        def mock_view_get(self, request, *args, **kwargs):
            response_mock = mock.MagicMock(spec=Response)
            response_mock.data = {'data': '12345'}
            return response_mock

        decorated_mock_view = custom_cache(
            key_prefix='prefix',
            model_kwargs={
                'entity_type__abreviation': 'entity_type',
                'pk': 'pk'
            }
        )(mock_view_get)

        decorated_mock_view(class_mock, request_mock, **kwargs)
        _get_obj_or_404.assert_called_once_with(
            ['queryset'],
            entity_type__abreviation='EST',
            pk='17'
        )

    @mock.patch('lupa.cache.django_cache')
    def test_retrive_data_from_cache_wo_no_role(self, _django_cache):
        """Return data from cache if user has no role and data has no
        group restrictions i.e no roles_allowed"""

        self.estado.roles_allowed.set([])
        self.estado.save()

        _django_cache.__contains__.return_value = True
        _django_cache.get.return_value = {'data': '12345'}
        request_mock = mock.MagicMock()

        payload = {
            'uid': 'username',

        }
        secret = config('SECRET_KEY')
        token = jwt.encode(payload, secret, algorithm="HS256")

        request_mock.GET = {'auth_token': token}

        class_mock = mock.MagicMock()
        class_mock.queryset = Entidade.objects.all()
        kwargs = {'entity_type': 'EST', 'domain_id': '1'}

        def mock_view_get(self, request, *args, **kwargs):
            return None

        decorated_mock_view = custom_cache(
            key_prefix='prefix', model_kwargs={'abreviation': 'entity_type'})(
            mock_view_get
        )

        response = decorated_mock_view(class_mock, request_mock, **kwargs)

        _django_cache.get.assert_called_once_with(
            'prefix:EST:1'
        )
        self.assertIsInstance(response, Response)
        self.assertEqual(response.data, {'data': '12345'})

    @mock.patch('lupa.cache.django_cache')
    def test_only_insert_response_200_in_cache(self, _django_cache):
        request_mock = mock.MagicMock()
        request_mock.GET = {'auth_token': 'abc1234'}
        class_mock = mock.MagicMock()
        class_mock.queryset = Entidade.objects.all()
        kwargs = {'entity_type': 'MUN', 'domain_id': '1'}

        def mock_view_get(self, request, *args, **kwargs):
            # spec: force mock to be Response class
            response_mock = mock.MagicMock(spec=Response)
            response_mock.data = {'data': '12345'}
            response_mock.status_code = 403
            return response_mock

        decorated_mock_view = custom_cache(
            key_prefix='prefix', model_kwargs={'abreviation': 'entity_type'})(
            mock_view_get
        )

        response = decorated_mock_view(class_mock, request_mock, **kwargs)

        _django_cache.set.assert_not_called()
        self.assertIsInstance(response, Response)


class ModelCache(TestCase):
    def setUp(self):
        self.role_allowed = 'role_allowed'
        self.entity_abrv = 'EST'
        self.entity_type = 'Estado'
        self.entity_name = 'Rio de Janeiro'
        self.entity_id = '1'

        municipio = make('lupa.Entidade', abreviation='MUN')
        self.grupo_allowed = make(
            'lupa.Grupo',
            role=self.role_allowed
        )
        estado = make(
            'lupa.Entidade',
            id=self.entity_id,
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

    @mock.patch('lupa.cache.django_cache')
    def test_only_cache_cacheable_objects(self, _django_cache):
        request_mock = mock.MagicMock()
        request_mock.GET = {'auth_token': 'abc1234'}
        class_mock = mock.MagicMock()
        class_mock.queryset = Entidade.objects.all()
        kwargs = {'entity_type': 'EST', 'domain_id': '1'}

        # non-cacheable
        self.estado.is_cacheable = False
        self.estado.save()

        def mock_view_get(self, request, *args, **kwargs):
            # spec: force mock to be Response class
            response_mock = mock.MagicMock(spec=Response)
            response_mock.data = {'data': '12345'}
            response_mock.status_code = 200
            return response_mock

        decorated_mock_view = custom_cache(
            key_prefix='prefix', model_kwargs={'abreviation': 'entity_type'})(
            mock_view_get
        )

        response = decorated_mock_view(class_mock, request_mock, **kwargs)

        _django_cache.set.assert_not_called()
        self.assertIsInstance(response, Response)

    @mock.patch('lupa.cache.django_cache')
    def test_cache_cacheable_object(self, _django_cache):
        request_mock = mock.MagicMock()
        request_mock.GET = {'auth_token': 'abc1234'}
        class_mock = mock.MagicMock()
        class_mock.queryset = Entidade.objects.all()
        kwargs = {'entity_type': 'EST', 'domain_id': '1'}

        def mock_view_get(self, request, *args, **kwargs):
            # spec: force mock to be Response class
            response_mock = mock.MagicMock(spec=Response)
            response_mock.data = {'data': '12345'}
            response_mock.status_code = 200
            return response_mock

        decorated_mock_view = custom_cache(
            key_prefix='prefix', model_kwargs={'abreviation': 'entity_type'})(
            mock_view_get
        )

        response = decorated_mock_view(class_mock, request_mock, **kwargs)

        _django_cache.set.assert_called_once_with(
            'prefix:EST:1', {'data': '12345'},
            timeout=None
        )
        self.assertIsInstance(response, Response)


class RepopulateCache(TestCase):
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
            cache_timeout=10
        )
        dado_2 = make(
            'lupa.DadoEntidade',
            pk=2,
            entity_type=municipio,
            order=7,
            cache_timeout=20
        )
        dado_3 = make(
            'lupa.DadoEntidade',
            pk=3,
            entity_type=estado,
            order=1,
            cache_timeout=30
        )
        dado_4 = make(
            'lupa.DadoEntidade',
            pk=4,
            entity_type=municipio,
            order=6,
            cache_timeout=40
        )

        queryset = DadoEntidade.objects.all()
        _repopulate_cache_data(
            key_prefix='lupa_dado_entidade',
            queryset=queryset,
            serializer=DadoEntidadeSerializer
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
            mock.call('key 1', {'id': dado_3.pk, 'exibition_field': None,
                                'external_data': {},
                                'data_type': dado_3.data_type.name,
                                'icon': None,
                                'detalhe': []},
                      timeout=dado_3.cache_timeout
                      ),
            mock.call('key 2', {'id': dado_3.pk, 'exibition_field': None,
                                'external_data': {},
                                'data_type': dado_3.data_type.name,
                                'icon': None,
                                'detalhe': []},
                      timeout=dado_3.cache_timeout
                      ),
            mock.call('key 3', {'id': dado_3.pk, 'exibition_field': None,
                                'external_data': {},
                                'data_type': dado_3.data_type.name,
                                'icon': None,
                                'detalhe': []},
                      timeout=dado_3.cache_timeout
                      ),
            mock.call('key 4', {'id': dado_3.pk, 'exibition_field': None,
                                'external_data': {},
                                'data_type': dado_3.data_type.name,
                                'icon': None,
                                'detalhe': []},
                      timeout=dado_3.cache_timeout
                      ),
            mock.call('key 5', {'id': dado_1.pk, 'exibition_field': None,
                                'external_data': {},
                                'data_type': dado_1.data_type.name,
                                'icon': None,
                                'detalhe': []},
                      timeout=dado_1.cache_timeout
                      ),
            mock.call('key 6', {'id': dado_1.pk, 'exibition_field': None,
                                'external_data': {},
                                'data_type': dado_1.data_type.name,
                                'icon': None,
                                'detalhe': []},
                      timeout=dado_1.cache_timeout
                      ),
            mock.call('key 7', {'id': dado_1.pk, 'exibition_field': None,
                                'external_data': {},
                                'data_type': dado_1.data_type.name,
                                'icon': None,
                                'detalhe': []},
                      timeout=dado_1.cache_timeout
                      ),
            mock.call('key 8', {'id': dado_1.pk, 'exibition_field': None,
                                'external_data': {},
                                'data_type': dado_1.data_type.name,
                                'icon': None,
                                'detalhe': []},
                      timeout=dado_1.cache_timeout
                      ),
            mock.call('key 9', {'id': dado_4.pk, 'exibition_field': None,
                                'external_data': {},
                                'data_type': dado_4.data_type.name,
                                'icon': None,
                                'detalhe': []},
                      timeout=dado_4.cache_timeout
                      ),
            mock.call('key 10', {'id': dado_4.pk, 'exibition_field': None,
                                 'external_data': {},
                                 'data_type': dado_4.data_type.name,
                                 'icon': None,
                                 'detalhe': []},
                      timeout=dado_4.cache_timeout
                      ),
            mock.call('key 11', {'id': dado_4.pk, 'exibition_field': None,
                                 'external_data': {},
                                 'data_type': dado_4.data_type.name,
                                 'icon': None,
                                 'detalhe': []},
                      timeout=dado_4.cache_timeout
                      ),
            mock.call('key 12', {'id': dado_4.pk, 'exibition_field': None,
                                 'external_data': {},
                                 'data_type': dado_4.data_type.name,
                                 'icon': None,
                                 'detalhe': []},
                      timeout=dado_4.cache_timeout
                      ),
            mock.call('key 13', {'id': dado_2.pk, 'exibition_field': None,
                                 'external_data': {},
                                 'data_type': dado_2.data_type.name,
                                 'icon': None,
                                 'detalhe': []},
                      timeout=dado_2.cache_timeout
                      ),
            mock.call('key 14', {'id': dado_2.pk, 'exibition_field': None,
                                 'external_data': {},
                                 'data_type': dado_2.data_type.name,
                                 'icon': None,
                                 'detalhe': []},
                      timeout=dado_2.cache_timeout
                      ),
            mock.call('key 15', {'id': dado_2.pk, 'exibition_field': None,
                                 'external_data': {},
                                 'data_type': dado_2.data_type.name,
                                 'icon': None,
                                 'detalhe': []},
                      timeout=dado_2.cache_timeout
                      ),
            mock.call('key 16', {'id': dado_2.pk, 'exibition_field': None,
                                 'external_data': {},
                                 'data_type': dado_2.data_type.name,
                                 'icon': None,
                                 'detalhe': []},
                      timeout=dado_2.cache_timeout
                      ),
        ]

        _execute_sample.assert_has_calls(execute_sample_calls)
        _cache_key.assert_has_calls(cache_key_calls)
        _django_cache.set.assert_has_calls(_django_cache_calls)

    @mock.patch('lupa.serializers.execute', return_value=None)
    @mock.patch('lupa.cache.execute_sample')
    @mock.patch('lupa.cache.cache_key')
    @mock.patch('lupa.cache.django_cache')
    def test_repopulate_cache_with_lupa_entidades(
            self,
            _django_cache,
            _cache_key,
            _execute_sample,
            _execute):

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
            serializer=EntidadeSerializer
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
            mock.call('key 1', {'domain_id': ('33001',),
                                'entity_type': estado.name,
                                'exibition_field': None,
                                'geojson': None, 'theme_list': []},
                      timeout=estado.cache_timeout
                      ),
            mock.call('key 2', {'domain_id': ('33010', ),
                                'entity_type': municipio.name,
                                'exibition_field': None,
                                'geojson': None, 'theme_list': []},
                      timeout=municipio.cache_timeout
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

        _execute_sample.assert_has_calls(execute_sample_calls)
        _cache_key.assert_has_calls(cache_key_calls)
        _django_cache.set.assert_has_calls(django_cache_calls)

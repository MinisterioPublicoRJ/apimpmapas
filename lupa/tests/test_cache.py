import jwt

from unittest import mock

from decouple import config
from django.test import TestCase
from model_mommy.mommy import make
from rest_framework.response import Response

from lupa.cache import cache_key, custom_cache, wildcard_cache_key
from lupa.models import Entidade


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

        make('lupa.Dado', id=1, entity_type=estado, theme=seguranca, order=2)
        make('lupa.Dado', id=2, entity_type=estado, theme=None, order=5)
        make('lupa.Dado', id=3, entity_type=municipio, order=7)
        make('lupa.Dado', id=4, entity_type=estado, theme=None, order=1)
        make('lupa.Dado', id=5, entity_type=estado, theme=saude, order=8)
        make('lupa.Dado', id=6, entity_type=municipio, order=6)
        make('lupa.Dado', id=7, entity_type=estado, theme=seguranca, order=3)
        make('lupa.Dado', id=8, entity_type=estado, theme=None, order=4)
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

        make('lupa.Dado', id=1, entity_type=estado, theme=seguranca, order=2)
        make('lupa.Dado', id=2, entity_type=estado, theme=None, order=5)
        make('lupa.Dado', id=3, entity_type=municipio, order=7)
        make('lupa.Dado', id=4, entity_type=estado, theme=None, order=1)
        make('lupa.Dado', id=5, entity_type=estado, theme=saude, order=8)
        make('lupa.Dado', id=6, entity_type=municipio, order=6)
        make('lupa.Dado', id=7, entity_type=estado, theme=seguranca, order=3)
        make('lupa.Dado', id=8, entity_type=estado, theme=None, order=4)
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

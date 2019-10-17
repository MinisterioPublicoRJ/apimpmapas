import jwt

from unittest import mock

from decouple import config
from django.test import TestCase
from django.urls import reverse
from model_mommy.mommy import make
from rest_framework.response import Response

from lupa.cache import cache_key, custom_cache


class Cache(TestCase):
    def setUp(self):
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

    @mock.patch('lupa.views._has_role', return_value=True)
    @mock.patch('lupa.views.django_cache')
    @mock.patch('lupa.serializers.execute')
    def test_insert_data_in_cache(self, _execute, _django_cache, _role):
        _execute.return_value = [('Rio de Janeiro', 'mock_geo')]

        url = reverse('lupa:detail_entidade', args=('EST', '33',))

        resp = self.client.get(url)
        resp_json = resp.json()

        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp_json, self.expected_answer)
        _django_cache.set.assert_called_once_with(
            'lupa_entidade:EST:33',
            self.expected_answer
        )

    @mock.patch('lupa.views._has_role', return_value=True)
    @mock.patch('lupa.views.EntidadeView.process_request')
    @mock.patch('lupa.views.django_cache')
    @mock.patch('lupa.serializers.execute')
    def test_retrieve_data_from_cache(self, _execute, _django_cache, _proc,
                                      _role):
        _django_cache.__contains__.return_value = True
        _django_cache.get.return_value = self.expected_answer
        _execute.return_value = [('Rio de Janeiro', 'mock_geo')]

        url = reverse('lupa:detail_entidade', args=('EST', '33',))

        resp = self.client.get(url)
        resp_json = resp.json()

        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp_json, self.expected_answer)
        _django_cache.get.assert_called_once_with(
            'lupa_entidade:EST:33',
        )
        _proc.assert_not_called()


class PermissionCache(TestCase):
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

    @mock.patch('lupa.views.django_cache')
    @mock.patch('lupa.serializers.execute')
    def test_donot_retrieve_data_from_cache_without_permission(
            self, _execute, _django_cache):

        _django_cache.__contains__.return_value = True
        _django_cache.get.return_value = self.expected_answer
        _execute.return_value = [('Rio de Janeiro', 'mock_geo')]
        payload = {
            'uid': 'username',
            'permissions': 'WithoutRole'
        }
        secret = config('SECRET_KEY')
        token = jwt.encode(payload, secret, algorithm="HS256")

        url = reverse('lupa:detail_entidade', args=('EST', '33',))
        url += '?auth_token=' + token.decode()

        resp = self.client.get(url)

        self.assertEqual(resp.status_code, 403)
        _django_cache.get.assert_not_called()

    @mock.patch('lupa.views.django_cache')
    @mock.patch('lupa.serializers.execute')
    def test_retrieve_data_from_cache_with_permission(self, _execute,
                                                      _django_cache):
        _django_cache.__contains__.return_value = True
        _django_cache.get.return_value = self.expected_answer
        _execute.return_value = [('Rio de Janeiro', 'mock_geo')]
        payload = {
            'uid': 'username',
            'permissions': 'role_allowed'
        }
        secret = config('SECRET_KEY')
        token = jwt.encode(payload, secret, algorithm="HS256")

        url = reverse('lupa:detail_entidade', args=('EST', '33',))
        url += '?auth_token=' + token.decode()

        resp = self.client.get(url)
        resp_json = resp.json()

        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp_json, self.expected_answer)
        _django_cache.get.assert_called_once_with('lupa_entidade:EST:33')


class DecoratorCache(TestCase):
    @mock.patch('lupa.cache.django_cache')
    def test_insert_data_in_cache(self, _django_cache):
        request_mock = mock.MagicMock()
        request_mock.GET.return_value = {'auth_token': 1234}
        kwargs = {'entity_type': 'MUN', 'domain_id': '1'}

        def mock_view_get(self, request, *args, **kwargs):
            # spec: force mock to be Response class
            response_mock = mock.MagicMock(spec=Response)
            response_mock.data = {'data': '12345'}
            return response_mock

        decorated_mock_view = custom_cache(key_prefix='prefix')(
            mock_view_get
        )

        response = decorated_mock_view(None, request_mock, **kwargs)

        _django_cache.set.assert_called_once_with(
            'prefix:MUN:1', {'data': '12345'}
        )
        self.assertIsInstance(response, Response)

    @mock.patch('lupa.cache.django_cache')
    def test_retrieve_data_from_cache(self, _django_cache):
        _django_cache.__contains__.return_value = True
        _django_cache.get.return_value = {'data': '12345'}
        request_mock = mock.MagicMock()
        request_mock.GET.return_value = {'auth_token': 1234}
        kwargs = {'entity_type': 'MUN', 'domain_id': '1'}

        def mock_view_get(self, request, *args, **kwargs):
            return None

        decorated_mock_view = custom_cache(key_prefix='prefix')(
            mock_view_get
        )

        response = decorated_mock_view(None, request_mock, **kwargs)

        _django_cache.get.assert_called_once_with(
            'prefix:MUN:1'
        )
        self.assertIsInstance(response, Response)
        self.assertEqual(response.data, {'data': '12345'})

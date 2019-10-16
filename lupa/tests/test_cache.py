from unittest import TestCase, mock

from rest_framework.response import Response

from lupa.cache import cache_key, custom_cache


class Cache(TestCase):
    def test_create_querystring_hash(self):
        token = 1234
        args_list = ['key 1']
        kwargs = {'key 1': 'MUN', 'key 2': 56789}

        key = cache_key(args_list, kwargs, token, key_prefix='key_prefix')
        expected_key = 'key_prefix_50491abb929620e598b27d56d101eef2_'\
            '81dc9bdb52d04dc20036dbd8313ed055'

        self.assertEqual(key, expected_key)

    @mock.patch('lupa.cache.cache_key', return_value='abcde')
    @mock.patch('lupa.cache.django_cache')
    def test_insert_data_in_cache(self, _django_cache, _cache_key):
        request_mock = mock.MagicMock()
        request_mock.GET = {'auth_token': 1234}
        kwargs = {'entity_type': 'MUN'}

        def mock_view_get(self, request, *args, **kwargs):
            # spec: force mock to be Response class
            response_mock = mock.MagicMock(spec=Response)
            response_mock.data = {'data': '12345'}
            return response_mock

        decorated_mock_view = custom_cache()(
            mock_view_get
        )
        response = decorated_mock_view(None, request_mock, **kwargs)

        _django_cache.set.assert_called_once_with(
            'abcde',
            {'data': '12345'},
            timeout=300
        )
        self.assertIsInstance(response, Response)

    @mock.patch('lupa.cache.cache_key', return_value='abcde')
    @mock.patch('lupa.cache.django_cache')
    def test_get_data_in_cache(self, _django_cache, _cache_key):
        request_mock = mock.MagicMock()
        request_mock.GET = {'auth_token': 1234}
        kwargs = {'entity_type': 'MUN'}
        _django_cache.get.return_value = {'data': '12345'}
        _django_cache.__contains__.return_value = True

        def mock_view_get(self, request, *args, **kwargs):
            return None  # If everything works this func won't be called

        decorated_mock_view = custom_cache()(
            mock_view_get
        )
        response = decorated_mock_view(None, request_mock, **kwargs)

        _django_cache.get.assert_called_once_with('abcde')
        self.assertIsInstance(response, Response)
        self.assertEqual(response.data, {'data': '12345'})

    @mock.patch('lupa.cache.cache_key', return_value='abcde')
    @mock.patch('lupa.cache.django_cache')
    def test_set_cache_timeout(self, _django_cache, _cache_key):
        request_mock = mock.MagicMock()
        request_mock.GET = {'auth_token': 1234}
        kwargs = {'entity_type': 'MUN'}

        # TODO: move this mock function outside tests
        def mock_view_get(self, request, *args, **kwargs):
            # spec: force mock to be Response class
            response_mock = mock.MagicMock(spec=Response)
            response_mock.data = {'data': '12345'}
            return response_mock

        decorated_mock_view = custom_cache(timeout=600)(
            mock_view_get
        )
        decorated_mock_view(None, request_mock, **kwargs)

        _django_cache.set.assert_called_once_with(
            'abcde',
            {'data': '12345'},
            timeout=600
        )

    @mock.patch('lupa.cache.django_cache')
    def test_set_cache_key_prefix(self, _django_cache):
        request_mock = mock.MagicMock()
        request_mock.GET = {'auth_token': 1234}
        kwargs = {'entity_type': 'MUN'}

        # TODO: move this mock function outside tests
        def mock_view_get(self, request, *args, **kwargs):
            # spec: force mock to be Response class
            response_mock = mock.MagicMock(spec=Response)
            response_mock.data = {'data': '12345'}
            return response_mock

        decorated_mock_view = custom_cache(key_prefix='key_prefix')(
            mock_view_get
        )
        decorated_mock_view(None, request_mock, **kwargs)

        _django_cache.set.assert_called_once_with(
            'key_prefix_50491abb929620e598b27d56d101eef2_'
            '81dc9bdb52d04dc20036dbd8313ed055',
            {'data': '12345'},
            timeout=300
        )

    @mock.patch('lupa.cache.django_cache')
    def test_set_cache_args_list(self, _django_cache):
        request_mock = mock.MagicMock()
        request_mock.GET = {'auth_token': 1234}
        kwargs = {'entity_type': 'MUN', 'pk': 1}

        # TODO: move this mock function outside tests
        def mock_view_get(self, request, *args, **kwargs):
            # spec: force mock to be Response class
            response_mock = mock.MagicMock(spec=Response)
            response_mock.data = {'data': '12345'}
            return response_mock

        decorated_mock_view = custom_cache(key_args=['entity_type', 'pk'])(
            mock_view_get
        )
        decorated_mock_view(None, request_mock, **kwargs)

        _django_cache.set.assert_called_once_with(
            '_b0a722932845b0c6871f6323fff36dd2_'
            '81dc9bdb52d04dc20036dbd8313ed055',
            {'data': '12345'},
            timeout=300
        )

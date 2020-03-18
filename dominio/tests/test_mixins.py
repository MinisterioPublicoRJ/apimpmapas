from unittest import mock, TestCase

from django.conf import settings
from django.core.paginator import EmptyPage
from django.http import HttpResponseForbidden
from jwt import DecodeError

from dominio.mixins import CacheMixin, JWTAuthMixin, PaginatorMixin


class TestMixins(TestCase):
    @mock.patch('dominio.mixins.Paginator')
    def test_paginate_mixin(self, _Paginator):
        paginator = PaginatorMixin()
        page_mock = mock.MagicMock()
        page_mock.page.return_value.object_list = 'object list'
        _Paginator.return_value = page_mock

        resp = paginator.paginate([1, 2, 3],  page=1, page_size=2)

        _Paginator.assert_called_once_with([1, 2, 3], 2)
        page_mock.page.assert_called_once_with(1)

        self.assertEqual(resp, 'object list')

    @mock.patch('dominio.mixins.Paginator')
    def test_paginate_mixin_empty_list(self, _Paginator):
        paginator = PaginatorMixin()
        page_mock = mock.MagicMock()
        page_mock.page.side_effect = EmptyPage
        _Paginator.return_value = page_mock

        resp = paginator.paginate([],  page=1, page_size=2)

        _Paginator.assert_called_once_with([], 2)
        page_mock.page.assert_called_once_with(1)

        self.assertEqual(resp, [])


class TestCacheMixin(TestCase):
    def test_cache_key(self):
        cache = CacheMixin()
        expected_cache_key = 'cache_mixin'

        self.assertEqual(cache.cache_key, expected_cache_key)

        cache.cache_key = 'another_cache'

        self.assertEqual(cache.cache_key, 'another_cache')

    def test_return_cache_key_with_correct_attr_name(self):
        cache = CacheMixin()
        expected_cache_key = 'cache_mixin'

        with self.assertRaises(AttributeError):
            cache.another_attr

        self.assertEqual(cache.cache_key, expected_cache_key)

    @mock.patch('%s.super' % __name__, create=True)
    @mock.patch('dominio.mixins.cache_page')
    def test_cached_dispatch_method(self, _cache_page, _super_func):
        dispatch_mock = mock.MagicMock()
        _cache_page.return_value = dispatch_mock

        class Parent:
            def dispatch(self, request, *args, **kwargs):
                pass

        class CacheChild(CacheMixin, Parent):
            pass

        cache_obj = CacheChild()
        cache_obj.dispatch('request', 1, 2, a=1, b=2)

        _cache_page.assert_called_once_with(
            cache_obj.get_timeout(),
            key_prefix=cache_obj.cache_key
        )
        dispatch_mock.assert_called()

    @mock.patch('dominio.mixins.config', return_value=100)
    def test_cache_config_string(self, _config):
        cache_obj = CacheMixin()
        cache_obj.cache_config = 'CACHE_CONFIG'

        timeout = cache_obj.get_timeout()

        self.assertEqual(timeout, 100)
        _config.assert_called_once_with(
            'CACHE_CONFIG',
            cast=int,
            default=settings.CACHE_TIMEOUT
        )

    def test_cache_config_none(self):
        cache_obj = CacheMixin()

        timeout = cache_obj.get_timeout()

        self.assertEqual(timeout, settings.CACHE_TIMEOUT)

    def test_user_cache_timeout(self):
        cache = CacheMixin()
        cache.cache_timeout = 100

        cache_timeout = cache.get_timeout()
        expected_cache_timeout = 100

        self.assertEqual(cache_timeout, expected_cache_timeout)


class TestJWTMixin(TestCase):
    @mock.patch('dominio.mixins.unpack_jwt')
    def test_call_unpack_jwt_before_dispatch(self, _unpack_jwt):
        class Parent:
            def dispatch(self, request, *args, **kwargs):
                pass

        class Child(JWTAuthMixin, Parent):
            def dispatch(self, request, *args, **kwargs):
                super().dispatch(request, *args, **kwargs)

        jwt_mixin = Child()
        jwt_mixin.dispatch('request')

        _unpack_jwt.assert_called_once_with('request')

    @mock.patch('dominio.mixins.unpack_jwt')
    def test_unpack_jwt_throw_error(self, _unpack_jwt):
        _unpack_jwt.side_effect = DecodeError

        class Parent:
            def dispatch(self, request, *args, **kwargs):
                pass

        class Child(JWTAuthMixin, Parent):
            def dispatch(self, request, *args, **kwargs):
                return super().dispatch(request, *args, **kwargs)

        jwt_mixin = Child()
        handler = jwt_mixin.dispatch('request')

        _unpack_jwt.assert_called_once_with('request')
        self.assertTrue(isinstance(handler, HttpResponseForbidden))

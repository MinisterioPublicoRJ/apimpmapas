from unittest import mock, TestCase

from django.core.paginator import EmptyPage

from dominio.mixins import CacheMixin, PaginatorMixin


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
        expected_cache_key = 'cache_mixin_key'

        self.assertEqual(cache.cache_key, expected_cache_key)

        cache.cache_key = 'another_cache_key'

        self.assertEqual(cache.cache_key, 'another_cache_key')

    def test_return_cache_key_with_correct_attr_name(self):
        cache = CacheMixin()
        expected_cache_key = 'cache_mixin_key'

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
            cache_obj.cache_timeout,
            key_prefix=cache_obj.cache_key
        )
        dispatch_mock.assert_called()

from unittest import mock, TestCase

from dominio.mixins import PaginatorMixin


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

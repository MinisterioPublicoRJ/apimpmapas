from unittest import mock

import pandas

from decouple import config
from django.shortcuts import reverse
from django.test import TestCase


class TestDesaparecidos(TestCase):
    @mock.patch('desaparecidos.views.search_target_person')
    @mock.patch('desaparecidos.views.client')
    @mock.patch('desaparecidos.views.cache')
    @mock.patch('desaparecidos.views.async_calculate_rank')
    def test_search_id_sinalid(self, _async_calculate_rank, _cache, _client,
                               _search):
        target_person = pandas.Series([1, 2, 3], index=['a', 'b', 'c'])
        _search.return_value = target_person
        _cache.get.return_value = None
        id_sinalid = '12345'
        url = reverse(
            'desaparecidos:busca',
            kwargs={'id_sinalid': id_sinalid}
        )

        resp = self.client.get(url)
        expected_resp = {'status': 'Seu pedido será processado'}

        _cache.get.assert_called_once_with(id_sinalid)
        _async_calculate_rank.delay.assert_called_once_with(
            id_sinalid,
            target_person
        )
        _cache.set.assert_called_once_with(
            id_sinalid,
            {'status': 'processing'}
        )
        self.assertEqual(resp.status_code, 201)
        self.assertEqual(resp.data, expected_resp)

    @mock.patch('desaparecidos.views.search_target_person')
    @mock.patch('desaparecidos.views.client')
    @mock.patch('desaparecidos.views.cache')
    @mock.patch('desaparecidos.views.async_calculate_rank')
    def test_search_processing_request(self, _async_calculate_rank, _cache,
                                       _client, _search):
        cache_resp = {'status': 'processing'}
        _cache.get.return_value = cache_resp
        id_sinalid = '12345'
        url = reverse(
            'desaparecidos:busca',
            kwargs={'id_sinalid': id_sinalid}
        )

        resp = self.client.get(url)

        _cache.get.assert_called_once_with(id_sinalid)
        _async_calculate_rank.delay.assert_not_called()
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.data, cache_resp)

    @mock.patch('desaparecidos.views.paginate')
    @mock.patch('desaparecidos.views.search_target_person')
    @mock.patch('desaparecidos.views.client')
    @mock.patch('desaparecidos.views.cache')
    @mock.patch('desaparecidos.views.async_calculate_rank')
    def test_search_ready(self, _async_calculate_rank, _cache, _client,
                          _search, _paginate):
        cache_resp = {'status': 'ready', 'data': [1, 2, 3, 4]}
        _paginate.return_value = [1, 2, 3, 4]
        _cache.get.return_value = cache_resp
        id_sinalid = '12345'
        url = reverse(
            'desaparecidos:busca',
            kwargs={'id_sinalid': id_sinalid}
        )

        resp = self.client.get(url)

        _cache.get.assert_called_once_with(id_sinalid)
        _async_calculate_rank.delay.assert_not_called()
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.data, cache_resp)

    @mock.patch('desaparecidos.views.search_target_person')
    @mock.patch('desaparecidos.views.client')
    @mock.patch('desaparecidos.views.cache')
    @mock.patch('desaparecidos.views.async_calculate_rank')
    def test_search_id_not_found(self, _async_calculate_rank, _cache, _client,
                                 _search):
        cursor_mock = mock.MagicMock()
        _client.return_value = cursor_mock
        _search.return_value = None
        cache_resp = {'status': 'Identificador Sinalid não encontrado'}
        _cache.get.return_value = cache_resp
        id_sinalid = 'not exist'
        url = reverse(
            'desaparecidos:busca',
            kwargs={'id_sinalid': id_sinalid}
        )

        resp = self.client.get(url)

        _client.assert_called_once_with(
            config('DESAPARECIDOS_DB_USER'),
            config('DESAPARECIDOS_DB_PWD'),
            config('DESAPARECIDOS_DB_HOST')
        )
        _search.assert_called_once_with(cursor_mock, id_sinalid)
        _cache.get.assert_not_called()
        _async_calculate_rank.delay.assert_not_called()
        self.assertEqual(resp.status_code, 404)
        self.assertEqual(resp.data, cache_resp)

    @mock.patch('desaparecidos.views.paginate')
    @mock.patch('desaparecidos.views.search_target_person')
    @mock.patch('desaparecidos.views.client')
    @mock.patch('desaparecidos.views.cache')
    @mock.patch('desaparecidos.views.async_calculate_rank')
    def test_search_paginate_default(self, _async_calculate_rank, _cache,
                                     _client, _search, _paginate):
        cache_resp = {'status': 'ready', 'data': [1, 2, 3, 4]}
        _paginate.return_value = [1, 2]
        _cache.get.return_value = cache_resp
        id_sinalid = '12345'
        url = reverse(
            'desaparecidos:busca',
            kwargs={'id_sinalid': id_sinalid}
        )

        resp = self.client.get(url)

        _cache.get.assert_called_once_with(id_sinalid)
        _async_calculate_rank.delay.assert_not_called()
        _paginate.assert_called_once_with(
            [1, 2, 3, 4],
            page=1,
            page_size=config('DESAPARECIDOS_PAGE_SIZE', cast=int)
        )
        expected_resp_data = {
            'status': 'ready',
            'data': [1, 2],
            '_links': {
                'first': 'http://localhost.com/desaparecidos/12345?page=1',
                'last': 'http://localhost.com/desaparecidos/12345?page=10',
                'next': 'http://localhost.com/desaparecidos/12345?page=2',
                'prev': None,
                'self': 'http://localhost.com/desaparecidos/12345?page=1',
            }
        }
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.data, expected_resp_data)

    @mock.patch('desaparecidos.views.paginate')
    @mock.patch('desaparecidos.views.search_target_person')
    @mock.patch('desaparecidos.views.client')
    @mock.patch('desaparecidos.views.cache')
    @mock.patch('desaparecidos.views.async_calculate_rank')
    def test_search_paginate_default_invalid_page(self, _async_calculate_rank,
                                                  _cache, _client, _search,
                                                  _paginate):
        cache_resp = {'status': 'ready', 'data': [1, 2, 3, 4]}
        _paginate.return_value = [1, 2]
        _cache.get.return_value = cache_resp
        id_sinalid = '12345'
        url = reverse(
            'desaparecidos:busca',
            kwargs={'id_sinalid': id_sinalid}
        )

        resp = self.client.get(url + '?page=invalid')

        _cache.get.assert_called_once_with(id_sinalid)
        _async_calculate_rank.delay.assert_not_called()
        _paginate.assert_called_once_with(
            [1, 2, 3, 4],
            page=1,
            page_size=config('DESAPARECIDOS_PAGE_SIZE', cast=int)
        )
        expected_resp_data = {
            'status': 'ready',
            'data': [1, 2],
            '_links': {
                'first': 'http://localhost.com/desaparecidos/12345?page=1',
                'last': 'http://localhost.com/desaparecidos/12345?page=10',
                'next': 'http://localhost.com/desaparecidos/12345?page=2',
                'prev': None,
                'self': 'http://localhost.com/desaparecidos/12345?page=1',
            }
        }
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.data, expected_resp_data)

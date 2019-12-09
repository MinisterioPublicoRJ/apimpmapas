from unittest import mock

from django.shortcuts import reverse
from django.test import TestCase


class TestDesaparecidos(TestCase):
    @mock.patch('desaparecidos.views.cache')
    @mock.patch('desaparecidos.views.async_calculate_rank')
    def test_search_id_sinalid(self, _async_calculate_rank, _cache):
        _cache.get.return_value = None
        id_sinalid = '12345'
        url = reverse(
            'desaparecidos:busca',
            kwargs={'id_sinalid': id_sinalid}
        )

        resp = self.client.post(url)
        expected_resp = {'status': 'Seu pedido será processado'}

        _cache.get.assert_called_once_with(id_sinalid)
        _async_calculate_rank.assert_called_once_with(id_sinalid)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.data, expected_resp)

    @mock.patch('desaparecidos.views.cache')
    @mock.patch('desaparecidos.views.async_calculate_rank')
    def test_search_processing_request(self, _async_calculate_rank, _cache):
        cache_resp = {'status': 'processing'}
        _cache.get.return_value = cache_resp
        id_sinalid = '12345'
        url = reverse(
            'desaparecidos:busca',
            kwargs={'id_sinalid': id_sinalid}
        )

        resp = self.client.post(url)

        _cache.get.assert_called_once_with(id_sinalid)
        _async_calculate_rank.assert_not_called()
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.data, cache_resp)

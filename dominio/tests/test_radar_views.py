from datetime import datetime
from decimal import Decimal
from unittest import mock

from django.conf import settings
from django.test import TestCase
from django.urls import reverse

from dominio.radar_queries import field_names
from dominio.radar_queries import query as radar_query


class TestSuaPromotoria(TestCase):
    @mock.patch("dominio.radar_views.run_query")
    def test_correct_response(self, _run_query):

        run_query_resp = [
            ('Tutela Coletiva',
             Decimal('123456'),
             179,
             25,
             12,
             0,
             0,
             datetime(2020, 3, 9, 14, 50, 11, 324000),
             '1ª PROMOTORIA DE JUSTIÇA',
             278,
             '2ª PROMOTORIA DE JUSTIÇA',
             151,
             '3ª PROMOTORIA DE JUSTIÇA',
             65,
             '4ª PROMOTORIA DE JUSTIÇA',
             10,
             '5ª PROMOTORIA DE JUSTIÇA',
             21,
             28,
             149,
             3,
             70,
             26,
             4,
             64.38848920863309,
             0.0,
             16.55629139072848,
             18.461538461538463,
             0.0,
             0.20134228187919462,
             0.0,
             -0.6428571428571429,
             -0.5384615384615384,
             0.0)
        ]
        _run_query.return_value = run_query_resp

        url = reverse('dominio:radar', args=('1', ))
        expected_data = (
            'Tutela Coletiva',
            Decimal('123456'),
            179,
            25,
            12,
            0,
            0,
            datetime(2020, 3, 9, 14, 50, 11, 324000),
            '1ª Promotoria de Justiça',
            278,
            '2ª Promotoria de Justiça',
            151,
            '3ª Promotoria de Justiça',
            65,
            '4ª Promotoria de Justiça',
            10,
            '5ª Promotoria de Justiça',
            21,
            28,
            149,
            3,
            70,
            26,
            4,
            64.38848920863309,
            0.0,
            16.55629139072848,
            18.461538461538463,
            0.0,
            0.20134228187919462,
            0.0,
            -0.6428571428571429,
            -0.5384615384615384,
            0.0)
        expected_resp = dict(zip(field_names, expected_data))

        resp = self.client.get(url)

        self.assertEqual(resp.status_code, 200)
        _run_query.assert_called_with(
            radar_query.format(schema=settings.TABLE_NAMESPACE),
            parameters={"orgao_id": 1}
        )
        self.assertEqual(resp.data, expected_resp)

    @mock.patch("dominio.radar_views.run_query")
    def test_404_response(self, _run_query):
        _run_query.return_value = None

        url = reverse('dominio:radar', args=('nonexist', ))

        resp = self.client.get(url)

        self.assertEqual(resp.status_code, 404)

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
            (
                'Tutela Coletiva',
                Decimal('123456'),
                179,
                25,
                12,
                0,
                0,
                datetime(2019, 3, 9, 14, 50, 11, 324000),
                28,
                278,
                151,
                65,
                10,
                21,
                149,
                3,
                70,
                32,
                4,
                64.38848920863309,
                0.0,
                16.55629139072848,
                18.461538461538463,
                0.0,
                0.20134228187919462,
                0.0,
                -0.6428571428571429,
                -0.625,
                0.0
            )
        ]
        _run_query.return_value = run_query_resp

        url = reverse('dominio:radar-suapromotoria', args=('1', ))
        expected_data = dict(zip(field_names, run_query_resp[0]))

        resp = self.client.get(url)

        self.assertEqual(resp.status_code, 200)
        _run_query.assert_called_with(
            radar_query.format(orgao_id=1, schema=settings.TABLE_NAMESPACE)
        )
        self.assertEqual(resp.data, expected_data)

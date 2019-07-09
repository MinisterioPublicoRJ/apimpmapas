import os

from django.test import TestCase
from django.urls import reverse

from model_mommy.mommy import make


class IntegrationTest(TestCase):
    def test_integration_view_postgres(self):
        if 'INTEGRATION_TEST' not in os.environ:
            self.skipTest(
                "Integration tests shouldn't be run along with unit tests"
            )

        make(
            'api.Dado',
            id=1,
            database='PG',
            columns=['total_homens', 'total_mulheres'],
            id_column='cod_est',
            schema='lupa',
            table='populacao_censo_est'
        )
        url = reverse(
            'api:detail_dado',
            kwargs={
                'domain_id': 33,
                'pk': 1
            }
        )

        resp = self.client.get(url)
        resp_json = resp.json()

        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp_json['external_data'], [[7625679.0, 8364250.0]])

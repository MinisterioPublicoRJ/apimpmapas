from unittest import mock

from django.conf import settings
from django.test import TestCase
from django.urls import reverse
from pysolr import SolrError
from rest_framework_simplejwt.tokens import AccessToken


class TestSolrPlacasViews(TestCase):
    def setUp(self):
        self.create_solr_client_patcher = mock.patch(
            "proxies.solr.views.create_solr_client"
        )
        self.create_solr_client_mock = self.create_solr_client_patcher.start()
        self.solr_client_mock = mock.Mock()
        self.data = {"response": "data"}
        self.solr_client_mock.search.return_value = self.data
        self.create_solr_client_mock.return_value = self.solr_client_mock

        access_token = AccessToken()
        access_token.payload["roles"] = (settings.PROXIES_PLACAS_ROLE,)
        access_token.payload["username"] = "username"
        self.token = str(access_token)
        self.url = reverse("proxies:solr-placas")

        self.dt_inicio = "2020-01-01T20:00:00"
        self.dt_fim = "2020-01-02T20:00:00"
        self.placa = "XXX1000"
        self.start = 1
        self.rows = 10

    def tearDown(self):
        self.create_solr_client_patcher.stop()

    def test_solr_placas_correct_response(self):
        resp = self.client.get(
            self.url,
            {
                "token": self.token,
                "placa": self.placa,
                "dt_inicio": self.dt_inicio,
                "dt_fim": self.dt_inicio,
                "start": self.start,
                "rows": self.rows,
            }
        )

        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.data, self.data)

    def test_solr_placas_invalid_role(self):
        token_obj = AccessToken()
        token_obj.payload["roles"] = ["wrong_ROLE"]
        token = str(token_obj)
        resp = self.client.get(
            self.url,
            {
                "token": token,
            }
        )

        self.assertEqual(resp.status_code, 403)

    def test_solr_placas_no_role(self):
        token = str(AccessToken())
        resp = self.client.get(
            self.url,
            {
                "token": token,
            }
        )

        self.assertEqual(resp.status_code, 403)

    def test_solr_client_error(self):
        self.solr_client_mock.search.side_effect = SolrError
        resp = self.client.get(
            self.url,
            {
                "token": self.token,
                "placa": self.placa,
                "dt_inicio": self.dt_inicio,
                "dt_fim": self.dt_inicio,
                "start": self.start,
                "rows": self.rows,
            }
        )

        self.assertEqual(resp.status_code, 503)

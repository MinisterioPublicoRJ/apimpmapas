from unittest import mock

from django.test import TestCase
from django.urls import reverse

from rest_framework_simplejwt.tokens import RefreshToken


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

        self.token = str(RefreshToken().access_token)
        self.url = reverse("proxies:solr-placas")
        self.query = "select * from dual"
        self.start = 1
        self.rows = 10

    def tearDown(self):
        self.create_solr_client_patcher.stop()

    def test_solr_placas_correct_response(self):
        resp = self.client.get(
            self.url,
            {
                "jwt": self.token,
                "query": self.query,
                "start": self.start,
                "rows": self.rows,
            }
        )

        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.data, self.data)

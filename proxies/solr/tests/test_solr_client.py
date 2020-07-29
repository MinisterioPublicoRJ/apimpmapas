import uuid
from unittest import TestCase, mock

import pysolr
from django.conf import settings

from proxies.solr.client import create_solr_client


class TestSolrClient(TestCase):
    def setUp(self):
        self.pysolr_zoo_patcher = mock.patch(
            "proxies.solr.client.pysolr.ZooKeeper"
        )
        self.zoo_mock = self.pysolr_zoo_patcher.start()
        self.zoo_mock.return_value = "zookeeper"
        self.pysolr_solr_patcher = mock.patch(
            "proxies.solr.client.pysolr.SolrCloud"
        )
        self.solr_mock = self.pysolr_solr_patcher.start()
        self.solr_mock.return_value = "solr connection"

    def tearDown(self):
        self.pysolr_zoo_patcher.stop()
        self.pysolr_solr_patcher.stop()

    def test_create_solr_client(self):
        solr_client = create_solr_client()

        self.zoo_mock.assert_called_once_with(settings.ZOOKEEPER_SERVER)
        self.solr_mock.assert_called_once_with(
            self.zoo_mock.return_value,
            settings.PLACAS_SOLR_COLLECTION,
            timeout=300,
        )
        self.assertEqual(solr_client._client, "solr connection")


class TestSolrQuery(TestCase):
    def setUp(self):
        self.pysolr_zoo_patcher = mock.patch(
            "proxies.solr.client.pysolr.ZooKeeper"
        )
        self.zoo_mock = self.pysolr_zoo_patcher.start()
        self.zoo_mock.return_value = "zookeeper"
        self.pysolr_solr_patcher = mock.patch(
            "proxies.solr.client.pysolr.SolrCloud"
        )

        self.data = [
            {
                "velocidade": "34",
                "lat": "-11.0000",
                "uuid": f"{uuid.uuid4()}",
                "lon": "-41.0000",
                "placa": "XXX1234",
                "datapassagem": "2020-03-09T14:04:12Z",
                "num_camera": "0000001",
                "faixa": "1",
                "_version_": 1111111111111111111111,
            },
            {
                "velocidade": "35",
                "lat": "-12.0000",
                "uuid": f"{uuid.uuid4()}",
                "lon": "-42.0000",
                "placa": "ZZZ9876",
                "datapassagem": "2020-03-20T19:04:09Z",
                "num_camera": "000002",
                "faixa": "1",
                "_version_": 22222222222222222,
            },
        ]
        self.resp = pysolr.Results(
            {"response": {"docs": self.data, "numFound": 2}}
        )
        self.solr_mock = self.pysolr_solr_patcher.start()

        self.solr_client_mock = mock.Mock(name="cliente")
        self.solr_client_mock.search.return_value = self.resp

        self.solr_mock.return_value = self.solr_client_mock

        self.query = "select * from dual"
        self.start = 1
        self.rows = 10

    def test_search_and_serialize_results(self):
        solr_client = create_solr_client()

        results = solr_client.search(
            self.query, start=self.start, rows=self.rows
        )

        self.assertEqual(results["docs"], self.data)
        self.assertEqual(results["numFound"], len(self.data))
        self.solr_client_mock.search.assert_called_once_with(
            self.query, start=self.start, rows=self.rows
        )
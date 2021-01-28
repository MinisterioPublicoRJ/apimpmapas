import uuid
from unittest import TestCase, mock

import pysolr
from django.conf import settings

from proxies.solr.client import SolrClient, create_solr_client


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

        self.kerberos_patcher = mock.patch(
            "proxies.solr.client.HTTPKerberosAuth"
        )
        self.kerberos_mock = self.kerberos_patcher.start()
        self.kerberos_auth_mock = mock.Mock()
        self.kerberos_mock.return_value = self.kerberos_auth_mock

    def tearDown(self):
        self.pysolr_zoo_patcher.stop()
        self.pysolr_solr_patcher.stop()
        self.kerberos_patcher.stop()

    def test_create_solr_client(self):
        solr_client = create_solr_client()

        self.zoo_mock.assert_called_once_with(settings.ZOOKEEPER_SERVER)
        self.solr_mock.assert_called_once_with(
            self.zoo_mock.return_value,
            settings.PLACAS_SOLR_COLLECTION,
            timeout=300,
            auth=self.kerberos_auth_mock,
        )
        self.assertEqual(solr_client._client, "solr connection")


class TestSolrClientRequest(TestCase):
    def setUp(self):
        response_mock = mock.Mock()
        response_mock.json.return_value = {"response": {"key": "data"}}
        self.requests_get_patcher = mock.patch(
            "proxies.solr.client.requests.get"
        )
        self.requests_get_mock = self.requests_get_patcher.start()
        self.requests_get_mock.return_value = response_mock

        self.kerberos_patcher = mock.patch(
            "proxies.solr.client.HTTPKerberosAuth"
        )
        self.kerberos_mock = self.kerberos_patcher.start()
        self.kerberos_auth_mock = mock.Mock()
        self.kerberos_mock.return_value = self.kerberos_auth_mock

        self.query = "solr query"
        self.expected = {'key': 'data'}

    def tearDown(self):
        self.kerberos_patcher.stop()
        self.requests_get_patcher.start()

    def test_query_with_requests(self):
        dados = SolrClient.request_query(self.query)

        self.assertEqual(dados, self.expected)
        self.requests_get_mock.assert_called_once_with(
            settings.HOST_SOLR + self.query,
            auth=self.kerberos_auth_mock
        )


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

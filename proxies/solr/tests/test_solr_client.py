from unittest import TestCase, mock

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

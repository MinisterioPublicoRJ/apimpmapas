import pysolr
from django.conf import settings
from requests_kerberos import HTTPKerberosAuth, REQUIRED


class SolrClient:
    def __init__(self, zookeeper, collection):
        kerberos_auth = HTTPKerberosAuth(
            mutual_authentication=REQUIRED,
            sanitize_mutual_error_response=False
        )
        self._client = pysolr.SolrCloud(
            zookeeper,
            collection,
            timeout=300,
            auth=kerberos_auth,
        )

    def search(self, query, start, rows):
        return self._client.search(query, start=start, rows=rows).raw_response[
            "response"
        ]


def create_solr_client():
    return SolrClient(
        pysolr.ZooKeeper(settings.ZOOKEEPER_SERVER),
        collection=settings.PLACAS_SOLR_COLLECTION,
    )

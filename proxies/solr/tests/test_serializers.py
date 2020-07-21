from django.test import TestCase

from proxies.solr.serializers import SolrPlacasSerializer


class TestSolrPlacas(TestCase):
    def setUp(self):
        self.query = "select * from dual"
        self.start = 1
        self.rows = 10
        self.data = {
            "query": self.query,
            "start": self.start,
            "rows": self.rows,
        }

    def test_validate_token_correct_response(self):
        ser = SolrPlacasSerializer(data=self.data)
        expected_validated_data = {
            "query": self.query,
            "start": self.start,
            "rows": self.rows,
        }
        is_valid = ser.is_valid()

        self.assertTrue(is_valid)
        self.assertEqual(ser.validated_data, expected_validated_data)

from django.conf import settings
from django.test import TestCase

from proxies.solr.serializers import SolrPlacasSerializer


class TestSolrPlacas(TestCase):
    def setUp(self):
        self.placa = "XXX1000"
        self.dt_inicio = "2020-01-01 12:00:00+00:00"
        self.dt_fim = "2020-01-10 12:00:00+00:00"
        self.start = 1
        self.rows = 10
        self.data = {
            "placa": self.placa,
            "dt_inicio": self.dt_inicio,
            "dt_fim": self.dt_fim,
            "start": self.start,
            "rows": self.rows,
        }

    def test_correct_response(self):
        ser = SolrPlacasSerializer(data=self.data)

        expected_query = (
            "datapassagem:[2020-01-01T12:00:00Z TO 2020-01-10T12:00:00Z]"
            f" AND placa:{self.placa}"
        )
        expected_validated_data = {
            "query": expected_query,
            "start": self.start,
            "rows": self.rows,
        }
        is_valid = ser.is_valid()

        self.assertTrue(is_valid)
        self.assertEqual(ser.validated_data, expected_validated_data)

    def test_maximum_rows(self):
        self.data["rows"] = settings.PLACAS_SOLR_MAX_ROWS + 1

        ser = SolrPlacasSerializer(data=self.data)
        is_valid = ser.is_valid()

        self.assertFalse(is_valid)

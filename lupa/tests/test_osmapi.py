import responses

from django.test import TestCase
from lupa.osmapi import (
    OsmQuery,
    OSM_APY
)
from unittest import mock
from .fixtures.osmapi import twoinoneout


class TestQuery(TestCase):

    @responses.activate
    def test_query(self):
        qjson = {
            "a": "b"
        }

        responses.add(
            "GET",
            "http://photon.komoot.de/api/",
            json=qjson
        )

        response = OsmQuery.objects._query("ilha do governador")

        self.assertEqual(response, qjson)
        self.assertEqual(
            responses.calls[0].request.url,
            OSM_APY + "?q=ilha+do+governador"
        )

    def test_filter(self):
        self.assertEqual(
            len(
                OsmQuery.objects._filter_response(
                    twoinoneout["features"]
                )
            ),
            2
        )

    @mock.patch.object(OsmQuery.objects, '_query', return_value=twoinoneout)
    def test_query_final(self, _query):
        querys = OsmQuery.objects.query("ilha do governador")

        _query.assert_called_with("ilha do governador")

        self.assertEqual(len(querys), 2)

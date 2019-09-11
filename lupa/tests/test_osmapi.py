import responses

from django.test import TestCase
from lupa import osmapi
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

        response = osmapi._query("ilha do governador")

        self.assertEqual(response, qjson)
        self.assertEqual(
            responses.calls[0].request.url,
            osmapi.OSM_APY + "?q=ilha+do+governador"
        )

    def test_filter(self):
        self.assertEqual(
            len(
                osmapi._filter_response(
                    twoinoneout["features"]
                )
            ),
            2
        )

    @mock.patch('lupa.osmapi._query', return_value=twoinoneout)
    def test_query_final(self, _query):
        querys = osmapi.query("ilha do governador")

        _query.assert_called_with("ilha do governador")

        self.assertEqual(len(querys), 2)

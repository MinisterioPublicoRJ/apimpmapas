import urllib.parse

import requests_mock
from django.conf import settings
from django.test import TestCase

from dominio.login.arcgis import get_token


class TestAuthArcGis(TestCase):
    def test_correct_response(self):
        response_json = {
            "token": "token",
            "expires": 1000,
            "ssl": True,
        }
        with requests_mock.Mocker() as mocked_request:
            mocked_request.post(
                settings.ARCGIS_TOKEN_ENDPOINT,
                json=response_json
            )
            resp = get_token()

        expected_payload = (
            f"username={settings.ARCGIS_TOKEN_USERNAME}&"
            f"password={settings.ARCGIS_TOKEN_PASSWORD}&"
            f"f={settings.ARCGIS_TOKEN_FORMAT}&"
            f"expiration={settings.ARCGIS_TOKEN_EXPIRATION}&"
            f"client={settings.ARCGIS_TOKEN_CLIENT}&"
            f"referer={settings.ARCGIS_TOKEN_REFERER}&"
            f"ip={settings.ARCGIS_TOKEN_IP}"
        )
        expected_resp = {
            "token": "token",
            "expires": 1000,
            "ssl": True,
        }

        self.assertEqual(resp, expected_resp)
        self.assertEqual(1, len(mocked_request.request_history))
        post_request = mocked_request.request_history[0]
        self.assertFalse(post_request.verify)
        self.assertEqual(
            expected_payload,
            urllib.parse.unquote(post_request.body)
        )

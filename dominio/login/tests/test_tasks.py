from unittest import mock

from django.conf import settings
from django.test import TestCase

from dominio.login.arcgis import ARCGIS_TOKEN_CACHE_KEY
from dominio.login.tasks import renew_arcgis_token


class TestRenewArcgisToken(TestCase):
    @mock.patch("dominio.login.tasks.cache")
    @mock.patch("dominio.login.tasks.get_token")
    def test_renew_arcgis_token(self, _get_token, _cache):
        resp = {
            "token": "token",
            "expiration": 1000,
            "ssl": True,
        }
        _get_token.return_value = resp

        renew_arcgis_token.run()

        _get_token.assert_called_once_with()
        _cache.set.assert_called_once_with(
            ARCGIS_TOKEN_CACHE_KEY,
            resp,
            timeout=settings.ARCGIS_TOKEN_EXPIRATION * 60
        )

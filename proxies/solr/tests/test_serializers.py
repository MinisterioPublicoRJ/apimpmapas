from unittest import mock

import pytest
from django.conf import settings
from django.test import TestCase
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework_simplejwt.exceptions import TokenError

from proxies.login.tokens import TokenDoesNotHaveRoleException
from proxies.solr.serializers import SolrPlacasSerializer


class TestSolrPlacas(TestCase):
    def setUp(self):
        self.token_obj = AccessToken()
        self.token_obj.payload["roles"] = (settings.PROXIES_PLACAS_ROLE,)
        self.jwt = str(self.token_obj)
        self.query = "select * from dual"
        self.start = 1
        self.rows = 10
        self.data = {
            "jwt": self.jwt,
            "query": self.query,
            "start": self.start,
            "rows": self.rows,
        }

    def test_validate_token_correct_response(self):
        ser = SolrPlacasSerializer(data=self.data)
        expected_validated_data = {
            "jwt": self.jwt,
            "query": self.query,
            "start": self.start,
            "rows": self.rows,
        }
        expected_validated_data.update(self.token_obj.payload)
        expected_validated_data["roles"] = [settings.PROXIES_PLACAS_ROLE]
        is_valid = ser.is_valid()

        self.assertTrue(is_valid)
        self.assertEqual(ser.validated_data, expected_validated_data)

    def test_invalid_role(self):
        token_obj = AccessToken()
        jwt = str(token_obj)
        self.data["jwt"] = jwt
        ser = SolrPlacasSerializer(data=self.data)

        with pytest.raises(TokenDoesNotHaveRoleException):
            ser.is_valid()

    @mock.patch("proxies.solr.serializers.SCAAccessToken")
    def test_invalid_token(self, _SCAAccessToken):
        _SCAAccessToken.side_effect = TokenError

        ser = SolrPlacasSerializer(data=self.data)

        self.assertFalse(ser.is_valid())

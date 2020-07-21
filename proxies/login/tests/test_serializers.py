from unittest import mock

import pytest
from django.core.exceptions import PermissionDenied
from django.test import TestCase

from proxies.login import serializers


class TestAccessTokenSerializers(TestCase):
    def setUp(self):
        self.sca_auth_patcher = mock.patch(
            "proxies.login.serializers.sca_authenticate"
        )
        self.sca_auth_mock = self.sca_auth_patcher.start()
        self.sca_auth_mock.return_value = {
            "logged_in": True,
            "permissions": ["ROLE_1", "ROLE_2"],
        }
        self.token_patcher = mock.patch(
            "proxies.login.serializers.SCAAccessToken"
        )
        self.token_mock = self.token_patcher.start()
        token_obj = mock.Mock(access_token="access token")
        token_obj.__str__ = lambda x:  "refresh token"
        self.token_mock.return_value = token_obj

        self.data = {"username": "username", "password": "pwd"}
        self.ser = serializers.SCATokenSerializer(data=self.data)

    def tearDown(self):
        self.sca_auth_patcher.stop()
        self.token_patcher.stop()

    def test_obtain_pair_token_happy_path(self):
        is_valid = self.ser.is_valid()

        self.assertTrue(is_valid)
        self.sca_auth_mock.assert_called_once_with(
            self.data["username"],
            self.data["password"],
            verify_roles=False
        )
        expected = {
            "access": "access token",
            "refresh": "refresh token"
        }

        self.assertEqual(self.ser.validated_data,  expected)

    def test_sca_permission_denied(self):
        self.sca_auth_mock.return_value = {"logged_in": False}
        with pytest.raises(PermissionDenied):
            self.ser.is_valid()

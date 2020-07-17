from unittest import mock

import pytest
from django.conf import settings
from django.core.exceptions import PermissionDenied
from django.test import TestCase
from rest_framework import serializers as drf_serializers

from proxies.login import serializers
from proxies.login.tokens import TokenDoesNotHaveRoleException


class TestAccessTokenSerializers(TestCase):
    def setUp(self):
        self.sca_auth_patcher = mock.patch(
            "proxies.login.serializers.sca_authenticate"
        )
        self.sca_auth_mock = self.sca_auth_patcher.start()
        self.sca_auth_mock.return_value = {"logged_in": True}
        self.token_patcher = mock.patch(
            "proxies.login.serializers.SCARefreshToken"
        )
        self.token_mock = self.token_patcher.start()
        token_obj = mock.Mock(access_token="access token")
        token_obj.__str__ = lambda x:  "refresh token"
        self.token_mock.return_value = token_obj

        self.data = {"username": "username", "password": "pwd"}
        self.ser = serializers.SCAJWTTokenSerializer(data=self.data)

    def tearDown(self):
        self.sca_auth_patcher.stop()
        self.token_patcher.stop()

    def test_obtain_pair_token_happy_path(self):
        is_valid = self.ser.is_valid()

        self.assertTrue(is_valid)
        self.sca_auth_mock.assert_called_once_with(
            self.data["username"],
            self.data["password"],
            roles=(settings.PROXIES_PLACAS_ROLE,)
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


class TestRefreshTokenSerializers(TestCase):
    def setUp(self):
        self.data = {"refresh": "refresh"}
        self.ser = serializers.SCAJWTRefreshTokenSerializer(data=self.data)
        self.token_patcher = mock.patch(
            "proxies.login.serializers.SCARefreshToken"
        )
        self.token_mock = self.token_patcher.start()
        token_obj = mock.Mock(
            access_token="access token",
            payload={"roles": (settings.PROXIES_PLACAS_ROLE,)},
        )
        self.token_mock.return_value = token_obj

    def test_refresh_token_happy_path(self):
        is_valid = self.ser.is_valid()

        self.assertTrue(is_valid)
        self.assertEqual(self.ser.validated_data["access"], "access token")
        self.token_mock.assert_called_once_with(self.data["refresh"])

    def test_invalid_role(self):
        self.token_mock.side_effect = TokenDoesNotHaveRoleException

        with pytest.raises(drf_serializers.ValidationError):
            self.ser.is_valid(raise_exception=True)

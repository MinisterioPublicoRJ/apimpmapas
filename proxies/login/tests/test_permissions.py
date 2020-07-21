from unittest import mock

import pytest
from django.test import TestCase
from rest_framework import serializers
from rest_framework.test import APIRequestFactory
from rest_framework_simplejwt.tokens import AccessToken

from proxies.login.permissions import SCARolePermission


class TestSCAPermission(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.view_roles = ["ROLE_1"]
        self.view = mock.Mock(permission_roles=self.view_roles)

        self.sca_permission = SCARolePermission()

    def test_valid_token_roles(self):
        username = "username"
        token_obj = AccessToken()
        token_obj.payload["roles"] = self.view_roles
        token_obj.payload["username"] = username
        token = str(token_obj)
        request = self.factory.get("/", {"token": token})
        has_perm = self.sca_permission.has_permission(request, self.view)

        self.assertTrue(has_perm)
        self.assertEqual(request.sca_username, username)

    def test_token_has_no_roles(self):
        token_obj = AccessToken()
        token = str(token_obj)
        request = self.factory.get("/", {"token": token})
        has_perm = self.sca_permission.has_permission(request, self.view)

        self.assertFalse(has_perm)
        self.assertFalse(hasattr(request, "sca_username"))

    def test_invalid_token_roles(self):
        token_obj = AccessToken()
        token_obj.payload["roles"] = ["wrong_ROLE"]
        token = str(token_obj)
        request = self.factory.get("/", {"token": token})
        has_perm = self.sca_permission.has_permission(request, self.view)

        self.assertFalse(has_perm)
        self.assertFalse(hasattr(request, "sca_username"))

    def test_no_token_provided(self):
        request = self.factory.get("/")
        with pytest.raises(serializers.ValidationError):
            self.sca_permission.has_permission(request, self.view)

        self.assertFalse(hasattr(request, "sca_username"))

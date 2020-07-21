from unittest import mock

import pytest
import jwt
from django.conf import settings
from django.test import TestCase
from rest_framework import serializers
from rest_framework.test import APIRequestFactory

from proxies.login.permissions import SCARolePermission


class TestSCAPermission(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.sca_roles = ["ROLE_1"]
        self.token = jwt.encode(
            {"roles": self.sca_roles},
            settings.JWT_SECRET,
            algorithm="HS256",
        )
        self.request = self.factory.get("/", {"token": self.token})
        self.view_roles = ["ROLE_1"]
        self.view = mock.Mock(permission_roles=self.view_roles)

        self.sca_permission = SCARolePermission()

    def test_valid_token_roles(self):
        has_perm = self.sca_permission.has_permission(self.request, self.view)

        self.assertTrue(has_perm)

    def test_token_has_no_roles(self):
        self.token = jwt.encode({}, settings.JWT_SECRET, algorithm="HS256")
        self.request = self.factory.get("/", {"token": self.token})
        has_perm = self.sca_permission.has_permission(self.request, self.view)

        self.assertFalse(has_perm)

    def test_invalid_token_roles(self):
        self.sca_roles = ["no_ROLE"]
        self.token = jwt.encode(
            {"roles": self.sca_roles},
            settings.JWT_SECRET,
            algorithm="HS256",
        )
        self.request = self.factory.get("/", {"token": self.token})
        has_perm = self.sca_permission.has_permission(self.request, self.view)

        self.assertFalse(has_perm)

    def test_no_token_provided(self):
        self.request = self.factory.get("/")
        with pytest.raises(serializers.ValidationError):
            self.sca_permission.has_permission(self.request, self.view)

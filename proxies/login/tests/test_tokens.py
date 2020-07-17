from unittest import TestCase

import pytest
from django.conf import settings
from rest_framework_simplejwt.tokens import RefreshToken

from proxies.login.tokens import SCARefreshToken, TokenDoesNotHaveRoleException


class TestRefreshToken(TestCase):
    def test_add_roles_to_payload(self):
        refresh = SCARefreshToken(username="username")

        self.assertEqual(
            refresh.payload["roles"],
            (settings.PROXIES_PLACAS_ROLE,),
        )
        self.assertEqual(
            refresh.payload["username"],
            "username"
        )

    def test_verify_valid_role(self):
        token_obj = RefreshToken()
        token_obj.payload["roles"] = (settings.PROXIES_PLACAS_ROLE,)
        token = str(token_obj)

        SCARefreshToken(token=token)

    def test_verify_invalid_role(self):
        token_obj = RefreshToken()
        token_obj.payload["roles"] = ("anoter role",)
        token = str(token_obj)

        with pytest.raises(TokenDoesNotHaveRoleException):
            SCARefreshToken(token=token)

    def test_verify_no_role(self):
        token = str(RefreshToken())

        with pytest.raises(TokenDoesNotHaveRoleException):
            SCARefreshToken(token=token)

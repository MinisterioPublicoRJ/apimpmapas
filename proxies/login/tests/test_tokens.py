from unittest import TestCase

from proxies.login.tokens import SCAAccessToken


class TestRefreshToken(TestCase):
    def test_add_username_and_roles_to_payload(self):
        username = "username"
        roles = ["role_1", "role_2"]
        refresh = SCAAccessToken(username=username, roles=roles)

        self.assertEqual(refresh.payload["roles"], roles)
        self.assertEqual(refresh.payload["username"], username)

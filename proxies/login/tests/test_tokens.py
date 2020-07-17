from unittest import TestCase

from django.conf import settings

from proxies.login.tokens import SCARefreshToken


class TestRefreshToken(TestCase):
    def test_add_roles_to_payload(self):
        refresh = SCARefreshToken()

        self.assertEqual(
            refresh.payload["roles"],
            (settings.PROXIES_PLACAS_ROLE,),
        )

from unittest import mock

from django.core.cache import cache

from dominio.mixins import JWTAuthMixin


class NoJWTTestCase:
    def setUp(self):
        self.mock_jwt = mock.patch('dominio.mixins.unpack_jwt')
        self.mock_authorize_in_orgao = mock.patch.object(
            JWTAuthMixin,
            "authorize_user_in_orgao"
        )
        super().setUp()
        self.mock_jwt.start()
        self.mocked_authorize = self.mock_authorize_in_orgao.start()
        self.mocked_authorize.return_value = True

    def tearDown(self):
        super().tearDown()
        self.mock_jwt.stop()
        self.mock_authorize_in_orgao.stop()


class NoCacheTestCase:
    def tearDown(self):
        cache.clear()

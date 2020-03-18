from unittest import mock

from django.core.cache import cache


class NoJWTTestCase:
    def setUp(self):
        self.mock_jwt = mock.patch('dominio.mixins.unpack_jwt')
        super().setUp()
        self.mock_jwt.start()

    def tearDown(self):
        super().tearDown()
        self.mock_jwt.stop()


class NoCacheTestCase:
    def tearDown(self):
        cache.clear()

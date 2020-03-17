from unittest import mock, TestCase

from login.jwtlogin import get_jwt_from_header


class TestJWTLogin(TestCase):
    def test_get_jwt_from_header(self):
        req_mock = mock.MagicMock()
        req_mock.headers = {'AUTHORIZATION': 'Bearer TOKEN'}

        token = get_jwt_from_header(req_mock)
        expected_token = 'TOKEN'

        self.assertEqual(token, expected_token)

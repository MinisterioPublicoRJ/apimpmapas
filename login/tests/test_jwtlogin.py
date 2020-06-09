from unittest import mock, TestCase

import pytest
from django.conf import settings
from jwt import DecodeError

from login.jwtlogin import (
    get_jwt_from_get,
    get_jwt_from_post,
    unpack_jwt,
    tipo_orgao,
)


class TestJWTLogin(TestCase):
    def test_get_jwt_from_get(self):
        req_mock = mock.MagicMock()
        req_mock.GET = {'jwt': 'TOKEN'}

        token = get_jwt_from_get(req_mock)
        expected_token = 'TOKEN'

        self.assertEqual(token, expected_token)

    def test_get_jwt_from_get_no_jwt_provided(self):
        req_mock = mock.MagicMock()
        req_mock.GET = dict()

        token = get_jwt_from_get(req_mock)
        expected_token = ''

        self.assertEqual(token, expected_token)

    def test_get_jwt_from_post(self):
        req_mock = mock.MagicMock()
        req_mock.POST = {'jwt': 'TOKEN'}

        token = get_jwt_from_post(req_mock)
        expected_token = 'TOKEN'

        self.assertEqual(token, expected_token)

    def test_get_jwt_from_post_no_jwt_provided(self):
        req_mock = mock.MagicMock()
        req_mock.POST = dict()

        token = get_jwt_from_post(req_mock)
        expected_token = ''

        self.assertEqual(token, expected_token)

    def test_tipo_orgao(self):
        nome_orgao_1 = "Tutela Coletiva"
        nome_orgao_2 = "Promotoria da Capital"
        nome_orgao_3 = "Tutela Coletiva da Infância"
        nome_orgao_4 = "Tutela Coletiva Idoso"

        tipo_orgao_1 = tipo_orgao(nome_orgao_1)
        tipo_orgao_2 = tipo_orgao(nome_orgao_2)
        tipo_orgao_3 = tipo_orgao(nome_orgao_3)
        tipo_orgao_4 = tipo_orgao(nome_orgao_4)

        self.assertEqual(tipo_orgao_1, 1)
        self.assertEqual(tipo_orgao_2, 0)
        self.assertEqual(tipo_orgao_3, 0)
        self.assertEqual(tipo_orgao_4, 0)

    @mock.patch('login.jwtlogin.jwt.decode', return_value="payload")
    @mock.patch('login.jwtlogin.get_jwt_from_get', return_value="TOKEN")
    def test_unpack_jwt(self, _get_jwt, _decode):
        resp = unpack_jwt('request')
        _get_jwt.assert_called_once_with('request')
        _decode.assert_called_once_with(
            "TOKEN",
            settings.JWT_SECRET,
            algorithm='HS256',
        )
        self.assertEqual(resp, "payload")

    @mock.patch('login.jwtlogin.get_jwt_from_get', return_value="")
    def test_unpack_no_jwt_provided(self, _get_jwt):
        request = mock.Mock()
        with pytest.raises(DecodeError):
            unpack_jwt(request)

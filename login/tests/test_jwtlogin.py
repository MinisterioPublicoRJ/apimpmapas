from unittest import mock, TestCase

from django.conf import settings

from login.jwtlogin import authenticate_integra, get_jwt_from_header


class TestJWTLogin(TestCase):
    def test_get_jwt_from_header(self):
        req_mock = mock.MagicMock()
        req_mock.headers = {'AUTHORIZATION': 'Bearer TOKEN'}

        token = get_jwt_from_header(req_mock)
        expected_token = 'TOKEN'

        self.assertEqual(token, expected_token)

    @mock.patch('login.jwtlogin.jwt.encode', return_value=b'encode_token')
    @mock.patch('login.jwtlogin.jwt.decode')
    @mock.patch('login.jwtlogin.get_jwt_from_header')
    def test_authenticate_integra(self, _get_jwt, _decode, _encode):
        _decode.return_value = {
            "user_name": "user_name",
            "scaUser": {
                "cpfUsuario": "123456789",
                "orgao": "1234",
                "pessDK": "4567",
                "nomeUsuario": "nome",
             }
        }
        jwt_payload = {
            "username": "user_name",
            "cpf": "123456789",
            "orgao": "1234",
            "pess_dk": "4567",
            "nome": "nome",
        }
        resp_payload = authenticate_integra('request')
        expected_payload = jwt_payload.copy()
        expected_payload["token"] = "encode_token"

        _get_jwt.assert_called_once_with('request')
        _encode.assert_called_once_with(
            jwt_payload,
            settings.JWT_SECRET,
            algorithm='HS256',
        )
        self.assertEqual(resp_payload, expected_payload)

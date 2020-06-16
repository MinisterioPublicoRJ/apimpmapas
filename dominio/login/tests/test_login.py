from datetime import date
from unittest import mock

import pytest
from django.conf import settings
from django.urls import reverse
from django.test import TestCase
from freezegun import freeze_time
from model_bakery.baker import make

from dominio.login.integra import authenticate_integra


@pytest.mark.django_db(transaction=True)
class TestLogin(TestCase):
    @mock.patch("dominio.models.RHFuncionario")
    @mock.patch("dominio.login.views.authenticate_integra")
    def test_correct_response(self, _auth_integra, _RhFuncionaio):
        mock_rh_obj = mock.Mock(sexo="X")
        _RhFuncionaio.objects.get.return_value = mock_rh_obj
        _auth_integra.return_value = {
            "username": "username",
            "matricula": "12345",
        }
        url = reverse("dominio:login")

        resp = self.client.post(url)
        expected_data = {
            "first_login": True,
            "first_login_today": True,
            "username": "username",
            "matricula": "12345",
            "sexo": "X",
        }

        self.assertEqual(resp.status_code, 200)
        _auth_integra.assert_called()
        self.assertEqual(resp.json(), expected_data)

    @mock.patch("dominio.models.RHFuncionario")
    @freeze_time('2020-01-01')
    @mock.patch("dominio.login.views.authenticate_integra")
    def test_user_already_logged_in(self, _auth_integra, _RhFuncionaio):
        mock_rh_obj = mock.Mock(sexo="X")
        _RhFuncionaio.objects.get.return_value = mock_rh_obj
        _auth_integra.return_value = {
            "username": "username",
            "matricula": "12345",
        }
        url = reverse("dominio:login")

        make("dominio.Usuario", username="username")

        with mock.patch("dominio.models.date") as date_mock:
            date_mock.today.return_value = date(2020, 1, 2)
            resp = self.client.post(url)
        expected_data = {
            "first_login": False,
            "first_login_today": True,
            "username": "username",
            "matricula": "12345",
            "sexo": "X",
        }

        self.assertEqual(resp.status_code, 200)
        _auth_integra.assert_called()
        self.assertEqual(resp.json(), expected_data)

    @mock.patch("dominio.models.RHFuncionario")
    @freeze_time('2020-01-01')
    @mock.patch("dominio.login.views.authenticate_integra")
    def test_user_already_logged_in_today(self, _auth_integra, _RhFuncionaio):
        mock_rh_obj = mock.Mock(sexo="X")
        _RhFuncionaio.objects.get.return_value = mock_rh_obj
        _auth_integra.return_value = {
            "username": "username",
            "matricula": "12345",
        }
        url = reverse("dominio:login")

        make("dominio.Usuario", username="username")

        with mock.patch("dominio.models.date") as date_mock:
            date_mock.today.return_value = date(2020, 1, 1)
            resp = self.client.post(url)
        expected_data = {
            "first_login": False,
            "first_login_today": False,
            "username": "username",
            "matricula": "12345",
            "sexo": "X",
        }

        self.assertEqual(resp.status_code, 200)
        _auth_integra.assert_called()
        self.assertEqual(resp.json(), expected_data)


class AuthenticateIntegraTest(TestCase):
    @mock.patch(
        'dominio.login.integra.jwt.encode', return_value=b'encode_token'
    )
    @mock.patch('dominio.login.integra.jwt.decode')
    @mock.patch('dominio.login.integra.get_jwt_from_post')
    def test_authenticate_integra(self, _get_jwt, _decode, _encode):
        _decode.return_value = {
            "user_name": "user_name",
            "scaUser": {
                "cpfUsuario": "123456789",
                "orgao": "1234",
                "pessDK": "4567",
                "nomeUsuario": "nome",
                "nomeOrgaoUsuario": "Tutela Coletiva",
                "matricula": "12345",
             }
        }
        jwt_payload = {
            "username": "user_name",
            "cpf": "123456789",
            "orgao": "1234",
            "pess_dk": "4567",
            "nome": "nome",
            "tipo_orgao": 1,
            "matricula": "12345",
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

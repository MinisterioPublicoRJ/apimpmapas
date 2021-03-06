from collections import namedtuple
from unittest import mock

from decouple import config
from django.test import TestCase
from django.urls import reverse

from login.sca import authenticate


class ScaTest(TestCase):
    def setUp(self):
        self.username = 'usuario'
        self.password = 'senha'
        self.return_ok = {
            'logged_in': True,
            'permissions': [config('LOGIN_ROLE')]
        }
        self.return_forbidden = {'logged_in': False}
        self.return_teapot = 418
        self.code_ok = 200
        self.permission_ok = {'permissions': {config('LOGIN_ROLE'): True}}
        self.permission_bad = {'permissions': {'ROLE_anyotherrole': True}}

    @mock.patch('login.sca.login')
    def test_login_correct(self, _login):
        respwrapper = namedtuple('Response', ['auth', 'info'])
        mock_auth = mock.MagicMock()
        mock_info = mock.MagicMock()
        mock_auth.status_code = self.code_ok
        mock_info.json.return_value = self.permission_ok
        _login.return_value = respwrapper(mock_auth, mock_info)

        auth_data = authenticate(self.username, self.password)

        _login.assert_called_once_with(
            self.username,
            bytes(self.password, 'utf-8'),
            config('SCA_AUTH'),
            config('SCA_CHECK')
        )
        self.assertEqual(auth_data, self.return_ok)

    @mock.patch('login.sca.login')
    def test_login_incorrect(self, _login):
        respwrapper = namedtuple('Response', ['auth', 'info'])
        mock_auth = mock.MagicMock()
        mock_info = None
        mock_auth.status_code = self.return_teapot
        _login.return_value = respwrapper(mock_auth, mock_info)

        auth_data = authenticate(self.username, self.password)

        _login.assert_called_once_with(
            self.username,
            bytes(self.password, 'utf-8'),
            config('SCA_AUTH'),
            config('SCA_CHECK')
        )
        self.assertEqual(auth_data, self.return_forbidden)

    @mock.patch('login.sca.login')
    def test_login_denied(self, _login):
        respwrapper = namedtuple('Response', ['auth', 'info'])
        mock_auth = mock.MagicMock()
        mock_info = mock.MagicMock()
        mock_auth.status_code = self.return_teapot
        mock_info.json.return_value = self.permission_bad
        _login.return_value = respwrapper(mock_auth, mock_info)

        auth_data = authenticate(self.username, self.password)

        _login.assert_called_once_with(
            self.username,
            bytes(self.password, 'utf-8'),
            config('SCA_AUTH'),
            config('SCA_CHECK')
        )
        self.assertEqual(auth_data, self.return_forbidden)


class LoginTest(TestCase):

    @mock.patch('login.views.jwt')
    @mock.patch('login.views.authenticate')
    def test_login_user(self, _auth, _jwt):
        _auth.return_value = {'logged_in': True, 'permissions': ['test_ROLE']}
        _jwt.encode.return_value = 'eyJ0eXAiOi'

        url = reverse('login:login')
        resp = self.client.post(
            url,
            data={
                'username': 'usuario',
                'password': 'senhaqq',
            }
        )

        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json(), 'eyJ0eXAiOi')

    @mock.patch('login.views.authenticate')
    def test_login_sca_failed(self, _auth):
        _auth.return_value = {'logged_in': False}
        url = reverse('login:login')
        resp = self.client.post(
            url,
            data={
                'username': 'usuario_nulo',
                'password': 'senhaqq',
            }
        )

        self.assertEqual(resp.status_code, 403)

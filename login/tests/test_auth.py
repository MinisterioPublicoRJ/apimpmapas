from unittest import mock

from django.test import TestCase
from django.urls import reverse

from login.decorators import auth_required


class LoginTest(TestCase):

    @mock.patch('login.views.jwt')
    @mock.patch('login.views.authenticate')
    def test_login_user(self, _auth, _jwt):
        _auth.return_value = 200
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
        _auth.return_value = 403
        url = reverse('login:login')
        resp = self.client.post(
            url,
            data={
                'username': 'usuario_nulo',
                'password': 'senhaqq',
            }
        )

        self.assertEqual(resp.status_code, 403)


class JWTDecoratorTest(TestCase):

    def test_valid_token(self):
        token = {'auth_token': 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.'
                 'eyJ1aWQiOiJFc3RldmFuIn0.'
                 'QsoGOa0S89KYUUpuwQ-QPq9cSSpuJdvxa3zYBeWcN1o'
                 }
        mock_request = mock.MagicMock()
        mock_request.GET.get.return_value = token['auth_token']

        def mock_config(*args, **kwargs):
            if args[0] == 'SECRET_KEY':
                return 'sfdfsdf'

        @auth_required
        def mock_view(*args, **kwargs):
            return True

        with mock.patch('login.decorators.config', side_effect=mock_config):
            resp = mock_view('args1', mock_request)

        self.assertEqual(resp, True)

    def test_invalid_token(self):
        token = {'auth_token': 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.'
                 'c3RldmFuI.SSpuJdvxa3'
                 }
        mock_request = mock.MagicMock()
        mock_request.GET.return_value = token

        @auth_required
        def mock_view(*args, **kwargs):
            return True

        resp = mock_view('args1', mock_request)

        self.assertEqual(resp.status_code, 403)

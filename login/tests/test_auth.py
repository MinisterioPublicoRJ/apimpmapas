from unittest import mock

from django.test import TestCase
from django.urls import reverse


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

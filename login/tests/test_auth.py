from unittest import mock

from django.test import TestCase
from django.urls import reverse


class LoginTest(TestCase):

    @mock.patch('login.views.authenticate')
    def test_login_user(self, _auth):
        _auth.return_value = 200

        url = reverse('login:login')
        resp = self.client.post(
            url,
            data={
                'username': 'usuario',
                'password': 'senhaqq',
            }
        )

        self.assertEqual(resp.status_code, 200)

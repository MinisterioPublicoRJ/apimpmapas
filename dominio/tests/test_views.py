from unittest import mock

from django.test import TestCase
from django.urls import reverse
from model_bakery.baker import make


class TestLogin(TestCase):
    @mock.patch("dominio.views.authenticate_integra")
    def test_correct_response(self, _auth_integra):
        _auth_integra.return_value = {"orgao": 12345}
        url = reverse("dominio:login")

        resp = self.client.post(url)
        expected_data = {
            "first_login": True,
            "first_login_today": True,
            "orgao": 12345,
        }

        self.assertEqual(resp.status_code, 200)
        _auth_integra.assert_called()
        self.assertEqual(resp.json(), expected_data)

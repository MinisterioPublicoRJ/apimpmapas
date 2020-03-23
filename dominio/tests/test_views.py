from datetime import date
from unittest import mock

import pytest
from django.test import TestCase
from django.urls import reverse
from freezegun import freeze_time
from model_bakery.baker import make


@pytest.mark.django_db(transaction=True)
class TestLogin(TestCase):
    @mock.patch("dominio.views.authenticate_integra")
    def test_correct_response(self, _auth_integra):
        _auth_integra.return_value = {"username": "username"}
        url = reverse("dominio:login")

        resp = self.client.post(url)
        expected_data = {
            "first_login": True,
            "first_login_today": True,
            "username": "username",
        }

        self.assertEqual(resp.status_code, 200)
        _auth_integra.assert_called()
        self.assertEqual(resp.json(), expected_data)

    @freeze_time('2020-01-01')
    @mock.patch("dominio.views.authenticate_integra")
    def test_user_already_logged_in(self, _auth_integra):
        _auth_integra.return_value = {"username": "username"}
        url = reverse("dominio:login")

        make("dominio.Usuario", username=12345)

        with mock.patch("dominio.models.date") as date_mock:
            date_mock.today.return_value = date(2020, 1, 2)
            resp = self.client.post(url)
        expected_data = {
            "first_login": False,
            "first_login_today": True,
            "username": "username",
        }

        self.assertEqual(resp.status_code, 200)
        _auth_integra.assert_called()
        self.assertEqual(resp.json(), expected_data)

    @freeze_time('2020-01-01')
    @mock.patch("dominio.views.authenticate_integra")
    def test_user_already_logged_in_today(self, _auth_integra):
        _auth_integra.return_value = {"username": "username"}
        url = reverse("dominio:login")

        make("dominio.Usuario", username="username")

        with mock.patch("dominio.models.date") as date_mock:
            date_mock.today.return_value = date(2020, 1, 1)
            resp = self.client.post(url)
        expected_data = {
            "first_login": False,
            "first_login_today": False,
            "username": "username",
        }

        self.assertEqual(resp.status_code, 200)
        _auth_integra.assert_called()
        self.assertEqual(resp.json(), expected_data)

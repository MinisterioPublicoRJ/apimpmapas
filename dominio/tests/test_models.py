from datetime import date
from unittest import mock, TestCase

import pytest
from freezegun import freeze_time

from dominio.models import Usuario


@pytest.mark.django_db(transaction=True)
class TestUsuario(TestCase):
    @freeze_time('2020-01-02')
    def test_create_last_login_field(self):
        usuario = Usuario.objects.create(
            username="username"
        )

        self.assertEqual(usuario.last_login, date(2020, 1, 2))

    @freeze_time('2020-01-01')
    def test_get_first_login_today(self):
        usuario = Usuario.objects.create(
            username="username",
            last_login=date(2020, 1, 1)
        )
        with mock.patch("dominio.models.date") as date_mock:
            date_mock.today.return_value = date(2020, 1, 2)
            first_time_today = usuario.get_first_login_today()

        self.assertTrue(first_time_today)

    @freeze_time('2020-01-01')
    def test_get_user_logged_in_today(self):
        usuario = Usuario.objects.create(
            username="username",
            last_login=date(2020, 1, 1)
        )
        with mock.patch("dominio.models.date") as date_mock:
            date_mock.today.return_value = date(2020, 1, 1)
            first_time_today = usuario.get_first_login_today()

        self.assertFalse(first_time_today)

    @mock.patch("dominio.models.RHFuncionario")
    def test_get_gender(self, _RhFuncionaio):
        mock_rh_obj = mock.Mock(sexo="X")
        _RhFuncionaio.objects.get.return_value = mock_rh_obj
        usuario = Usuario.objects.create(
            username="user_name",
        )

        gender = usuario.get_gender(cdmatricula="12345")

        self.assertEqual(gender, "X")

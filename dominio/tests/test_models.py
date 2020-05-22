from datetime import date
from unittest import mock, TestCase

import pytest
from django.conf import settings
from freezegun import freeze_time

from dominio.models import Alerta, Usuario


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


class TestAlertaModels(TestCase):
    @mock.patch("dominio.models.run_query")
    def test_validos_por_orgaos(self, _run_query):
        orgao_id = 12345
        _run_query.return_value = [
            (
                'data 1',
                'data 2',
                0,
                'data 3',
                'data 4',
                'data 5',
                'data 6',
                'data 7',
                int(orgao_id),
                'data 8',
                -1,
            )
        ]
        resp = Alerta.validos_por_orgao(orgao_id)
        expected_resp = [
            {
                'doc_dk': 'data 1',
                'num_doc': 'data 2',
                'num_ext': 0,
                'etiqueta': 'data 3',
                'classe_doc': 'data 4',
                'data_alerta': 'data 5',
                'orgao': 'data 6',
                'classe_hier': 'data 7',
                'dias_passados': 12345,
                'descricao': 'data 8',
                'sigla': -1}
        ]

        _run_query.assert_called_once_with(
            Alerta.query_base.format(schema=settings.TABLE_NAMESPACE),
            {"orgao_id": orgao_id},
        )
        self.assertEqual(resp, expected_resp)

    @mock.patch("dominio.models.run_query")
    def test_validos_por_orgaos_tipo(self, _run_query):
        orgao_id = 12345
        tipo_alerta = 'ALRT'
        _run_query.return_value = [
            (
                'data 1',
                'data 2',
                0,
                'data 3',
                'data 4',
                'data 5',
                'data 6',
                'data 7',
                int(orgao_id),
                'data 8',
                -1,
            )
        ]
        resp = Alerta.validos_por_orgao(orgao_id, tipo_alerta)
        expected_resp = [
            {
                'doc_dk': 'data 1',
                'num_doc': 'data 2',
                'num_ext': 0,
                'etiqueta': 'data 3',
                'classe_doc': 'data 4',
                'data_alerta': 'data 5',
                'orgao': 'data 6',
                'classe_hier': 'data 7',
                'dias_passados': 12345,
                'descricao': 'data 8',
                'sigla': -1}
        ]

        _run_query.assert_called_once_with(
            Alerta.query_tipo.format(schema=settings.TABLE_NAMESPACE),
            {"orgao_id": orgao_id, "tipo_alerta": tipo_alerta},
        )
        self.assertEqual(resp, expected_resp)


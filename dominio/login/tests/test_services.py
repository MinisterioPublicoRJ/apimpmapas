from datetime import date
from unittest import mock

import pytest
from django.test import TestCase
from freezegun import freeze_time
from model_bakery import baker

from dominio.exceptions import UserHasNoValidOfficesError
from dominio.login import services
from dominio.models import Usuario


class PromotronLoginServices(TestCase):
    def setUp(self):
        self.TEST_DATABASE_NAME = "default"
        self.username = "username"

        self.jwt_patcher = mock.patch(
            "dominio.login.services.jwt.encode", return_value="auth-token"
        )
        self.jwt_mock = self.jwt_patcher.start()
        self.oracle_access_patcher = mock.patch(
            "dominio.login.dao.oracle_access"
        )
        self.mock_oracle_access = self.oracle_access_patcher.start()
        self.mock_oracle_access.side_effect = [
            (
                (
                    "098765",
                    "12345",
                    "123456789",
                    "NOME FUNCIONARIO",
                    "X",
                    "4567",
                    "PROMOTORIA INVESTIGAÇÃO PENAL",
                    None,
                    "RE",
                ),
                (
                    "1234",
                    "12345",
                    "123456789",
                    "NOME FUNCIONARIO",
                    "X",
                    "4567",
                    "PROMOTORIA DIFERENTE",
                    None,
                    "RE",
                ),
            ),
            (
                ("1234", "PROMOTORIA TUTELA COLETIVA", None, "RE"),
            ),  # result set do lista orgao pessoal
        ]
        self.expected_response = {
            "username": self.username,
            "cpf": "123456789",
            "orgao": "098765",
            "pess_dk": "4567",
            "nome": "NOME FUNCIONARIO",
            "tipo_orgao": 2,
            "matricula": "12345",
            "first_login": True,
            "first_login_today": True,
            "sexo": "X",
            "token": "auth-token",
            "orgaos_validos": [
                {
                    "orgao": "PROMOTORIA INVESTIGAÇÃO PENAL",
                    "tipo": 2,
                    "cdorgao": "098765",
                },
                {
                    "orgao": "PROMOTORIA TUTELA COLETIVA",
                    "tipo": 1,
                    "cdorgao": "1234",
                },
            ],
        }

    def tearDown(self):
        self.oracle_access_patcher.stop()
        self.jwt_patcher.stop()

    def test_classify_orgaos(self):
        """Um promotor pode estar lotado em mais de um órgao.
        Essa função irá dizer o tipo_orgao de cada uma deles"""
        lista_orgaos = (
            {
                "cdorgao": "1234",
                "matricula": "12345",
                "cpf": "123456789",
                "nome": "NOME FUNCIONARIO",
                "sexo": "X",
                "pess_dk": "4567",
                "nm_org": "PROMOTORIA TUTELA COLETIVA",
                "grupo": None,
                "atrib": "RE",
            },
            {
                "cdorgao": "1234",
                "matricula": "12345",
                "cpf": "123456789",
                "nome": "NOME FUNCIONARIO",
                "sexo": "X",
                "pess_dk": "4567",
                "nm_org": "PROMOTORIA DIFERENTE",
                "grupo": None,
                "atrib": "RE",
            },
            # resposta de ListaOrgaoPessoal
            {
                "cdorgao": "1234",
                "nm_org": "PROMOTORIA INVESTIGAÇÃO PENAL",
                "grupo": None,
                "atrib": "RE",
            },
        )

        tipos_promotorias = services.classifica_orgaos(lista_orgaos)
        expected = [
            {
                "orgao": "PROMOTORIA TUTELA COLETIVA",
                "tipo": 1,
                "cdorgao": "1234",
            },
            {
                "orgao": "PROMOTORIA DIFERENTE",
                "tipo": 0,
                "cdorgao": "1234",
            },
            {
                "orgao": "PROMOTORIA INVESTIGAÇÃO PENAL",
                "tipo": 2,
                "cdorgao": "1234",
            },
        ]

        self.assertEqual(tipos_promotorias, expected)

    def test_get_filter_valid_orgaos(self):
        """Esta função dirá quais os orgaos que um servidor está lotado são
        válidos. Até o momento, órgãoes com tipo != 0 são válidos."""
        lista_orgaos = [
            {
                "orgao": "PROMOTORIA TUTELA COLETIVA",
                "tipo": 1,
                "cdorgao": "1234",
            },
            {
                "orgao": "PROMOTORIA DIFERENTE",
                "tipo": 0,
                "cdorgao": "1234",
            },
            {
                "orgao": "PROMOTORIA INVESTIGAÇÃO PENAL",
                "tipo": 2,
                "cdorgao": "1234",
            },
        ]

        orgao = services.filtra_orgaos_validos(lista_orgaos)
        expected = [
            {
                "orgao": "PROMOTORIA TUTELA COLETIVA",
                "tipo": 1,
                "cdorgao": "1234",
            },
            {
                "orgao": "PROMOTORIA INVESTIGAÇÃO PENAL",
                "tipo": 2,
                "cdorgao": "1234",
            },
        ]

        self.assertEqual(orgao, expected)

    def test_build_login_response(self):
        response = services.build_login_response(self.username)

        for key in response.keys():
            with self.subTest():
                self.assertEqual(
                    response[key], self.expected_response[key], key
                )

    @mock.patch("dominio.login.services.classifica_orgaos")
    def test_nenhum_orgao_valido_encontrado(self, _classifica_orgaos):
        # nenhum orgao valio
        _classifica_orgaos.return_value = [
            {"orgao": "ORGAO INVALIDO", "tipo": 0}
        ]

        with pytest.raises(UserHasNoValidOfficesError):
            services.build_login_response("username")

    def test_nenhum_orgao_encontrado_no_mgp(self):
        self.mock_oracle_access.side_effect = [(), ]

        with pytest.raises(UserHasNoValidOfficesError):
            services.build_login_response("username")

    def test_update_user_first_login_today(self):
        with freeze_time("2020-1-1"):  # date of user creation in DB
            user_db = baker.make(Usuario, username=self.username)


        with freeze_time("2020-7-1"):  # date of login
            response = services.build_login_response(self.username)

        self.expected_response["first_login"] = False
        self.expected_response["first_login_today"] = True


        for key in response.keys():
            with self.subTest():
                self.assertEqual(
                    response[key], self.expected_response[key], key
                )

        user_db.refresh_from_db(using=self.TEST_DATABASE_NAME)
        self.assertEqual(user_db.last_login, date(2020, 7, 1))

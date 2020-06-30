from unittest import mock

import pytest
from django.test import TestCase

from dominio.exceptions import UserHasNoValidOfficesError
from dominio.login import services


class PromotronLoginServices(TestCase):
    def setUp(self):
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

    def tearDown(self):
        self.mock_oracle_access.stop()

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

    @mock.patch("dominio.login.services.jwt.encode", return_value="auth-token")
    def test_build_login_response(self, _jwt_encode):
        username = "username"

        response = services.build_login_response(username)
        expected_response = {
            "username": username,
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

        for key in response.keys():
            with self.subTest():
                self.assertEqual(
                    response[key], expected_response[key], key
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

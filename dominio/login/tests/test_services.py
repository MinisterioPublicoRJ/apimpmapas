from datetime import date
from unittest import mock

import pytest
from django.test import TestCase, override_settings
from freezegun import freeze_time
from model_bakery import baker

from dominio.login import services, exceptions
from dominio.models import Usuario


class TestBuildLoginResponse(TestCase):
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
        self.oracle_return_dados_usuario = (
            ("12345", "123456789", "NOME FUNCIONARIO", "X", "4567"),
        )
        self.mock_oracle_access.side_effect = [
            self.oracle_return_dados_usuario,
            (
                ("098765", "PROMOTORIA INVESTIGAÇÃO PENAL"),
                ("1234", "PROMOTORIA DIFERENTE"),
            ),
            (
                ("1234", "PROMOTORIA TUTELA COLETIVA"),
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
                    "cpf": "123456789",
                    "matricula": "12345",
                    "pess_dk": "4567",
                    "nome": "NOME FUNCIONARIO",
                    "sexo": "X",
                    "nm_org": "PROMOTORIA INVESTIGAÇÃO PENAL",
                    "tipo": 2,
                    "cdorgao": "098765",
                },
                {
                    "cpf": "123456789",
                    "matricula": "12345",
                    "pess_dk": "4567",
                    "nome": "NOME FUNCIONARIO",
                    "sexo": "X",
                    "nm_org": "PROMOTORIA TUTELA COLETIVA",
                    "tipo": 1,
                    "cdorgao": "1234",
                },
            ],
        }
        self.username = "username"
        self.permissoes = services.PermissoesUsuarioRegular(
            username=self.username
        )

    def tearDown(self):
        self.oracle_access_patcher.stop()
        self.jwt_patcher.stop()

    def test_build_login_response(self):
        response = services.build_login_response(self.permissoes)

        for key in response.keys():
            with self.subTest():
                self.assertEqual(
                    response[key], self.expected_response[key], key
                )

    def test_nenhum_orgao_encontrado_no_mgp(self):
        self.mock_oracle_access.side_effect = [
            self.oracle_return_dados_usuario,
            (),
        ]

        with pytest.raises(exceptions.UserHasNoOfficeInformation):
            services.build_login_response(self.permissoes)

    def test_update_user_first_login_today(self):
        with freeze_time("2020-1-1"):  # date of user creation in DB
            user_db = baker.make(Usuario, username=self.username)

        with freeze_time("2020-7-1"):  # date of login
            response = services.build_login_response(self.permissoes)

        self.expected_response["first_login"] = False
        self.expected_response["first_login_today"] = True

        for key in response.keys():
            with self.subTest():
                self.assertEqual(
                    response[key], self.expected_response[key], key
                )

        user_db.refresh_from_db(using=self.TEST_DATABASE_NAME)
        self.assertEqual(user_db.last_login, date(2020, 7, 1))

    def test_NOT_first_login_today(self):
        with freeze_time("2020-1-1"):  # date of user creation in DB
            user_db = baker.make(Usuario, username=self.username)

        with freeze_time("2020-1-1"):  # date of login
            response = services.build_login_response(self.permissoes)

        self.expected_response["first_login"] = False
        self.expected_response["first_login_today"] = False

        for key in response.keys():
            with self.subTest():
                self.assertEqual(
                    response[key], self.expected_response[key], key
                )

        user_db.refresh_from_db(using=self.TEST_DATABASE_NAME)
        self.assertEqual(user_db.last_login, date(2020, 1, 1))


class TestPermissoesUsuarioRegular(TestCase):
    def setUp(self):
        self.username = "username"
        self.oracle_access_patcher = mock.patch(
            "dominio.login.dao.oracle_access"
        )
        self.mock_oracle_access = self.oracle_access_patcher.start()
        self.oracle_return_dados_usuario = (
            ("12345", "123456789", "NOME FUNCIONARIO", "X", "4567"),
        )
        self.oracle_return_lista_orgao = (
            ("098765", "PROMOTORIA INVESTIGAÇÃO PENAL"),
            ("1234", "PROMOTORIA DIFERENTE"),
        )
        self.oracle_return_lista_orgao_pessoal = (
            ("9999", "PROMOTORIA TUTELA COLETIVA"),
        )
        self.mock_oracle_access.side_effect = [
            self.oracle_return_lista_orgao,
            self.oracle_return_lista_orgao_pessoal,
            self.oracle_return_dados_usuario,
        ]
        self.expected = [
            {
                "cpf": "123456789",
                "pess_dk": "4567",
                "nome": "NOME FUNCIONARIO",
                "matricula": "12345",
                "sexo": "X",
                "cdorgao": "098765",
                "nm_org": "PROMOTORIA INVESTIGAÇÃO PENAL",
                "tipo": 2,
            },
            {
                "cpf": "123456789",
                "pess_dk": "4567",
                "nome": "NOME FUNCIONARIO",
                "matricula": "12345",
                "sexo": "X",
                "cdorgao": "1234",
                "nm_org": "PROMOTORIA DIFERENTE",
                "tipo": 0,
            },
            {
                "cpf": "123456789",
                "pess_dk": "4567",
                "nome": "NOME FUNCIONARIO",
                "matricula": "12345",
                "sexo": "X",
                "cdorgao": "9999",
                "nm_org": "PROMOTORIA TUTELA COLETIVA",
                "tipo": 1,
            },
        ]
        self.permissoes = services.PermissoesUsuarioRegular(
            username=self.username
        )

    def tearDown(self):
        self.oracle_access_patcher.stop()

    def test_retorna_orgaos_de_usuario(self):
        self.assertEqual(self.permissoes.orgaos_lotados, self.expected)

    def test_retorna_orgaos_VALIDOS_de_usuario(self):
        """Retorna orgaos validos (do ponto de vista do Promotron).
        Até o momento PIP e Tutela (com excessão de infância e idoso)
        """
        self.expected.pop(1)
        self.assertEqual(self.permissoes.orgaos_validos, self.expected)

    def test_ListOrgaoDao_NAO_pode_estar_vazio(self):
        self.mock_oracle_access.side_effect = [
            [],
            self.oracle_return_lista_orgao_pessoal,
        ]

        with pytest.raises(exceptions.UserHasNoOfficeInformation):
            self.permissoes.orgaos_lotados

    def test_ListOrgaoPessoalDao_pode_estar_vazio(self):
        self.mock_oracle_access.side_effect = [
            self.oracle_return_lista_orgao,
            [],
            self.oracle_return_dados_usuario,
        ]
        lista_orgaos = self.permissoes.orgaos_lotados

        self.expected.pop(-1)  # remove resposta vazia
        self.assertEqual(lista_orgaos, self.expected)

    def test_classifica_orgaos(self):
        """Um promotor pode estar lotado em mais de um órgao.
        Essa função irá dizer o tipo_orgao de cada uma deles"""
        lista_orgaos = self.expected.copy()
        tipos_promotorias = self.permissoes._classifica_orgaos(lista_orgaos)
        expected = self.expected.copy()
        expected[0]["tipo"] = 2
        expected[1]["tipo"] = 0
        expected[2]["tipo"] = 1

        self.assertEqual(tipos_promotorias, expected)

    def test_filtra_orgaos_invalidos(self):
        lista_orgaos = self.expected.copy()
        lista_orgaos[0]["tipo"] = 2
        lista_orgaos[1]["tipo"] = 0
        lista_orgaos[2]["tipo"] = 1

        tipos_promotorias = self.permissoes._filtra_orgaos_invalidos(
            lista_orgaos
        )

        expected = self.expected.copy()
        expected.pop(1)  # Remove órgão inválido (tipo = 0)

        self.assertEqual(tipos_promotorias, expected)

    def test_erro_se_resposta_do_banco_nao_conter_dados_do_usuario(self):
        # Resposa da query ListaOrgao não possui órgão válido, portanto
        # não pode ser usado pra dados do usuário.
        # Resposta da query ListaOrgaoPessoal não traz informações do usuário
        self.mock_oracle_access.side_effect = [
            (),  # Dados do usuário
        ]
        with pytest.raises(exceptions.UserDetailsNotFoundError):
            self.permissoes.dados_usuario

    def test_determina_um_orgao_valido_dentre_os_retornados_pelo_bd(self):
        """Um usuário pode estar lotado em mais de um órgão válido.
        Este método deve selcionar um deles"""
        orgao_selecionado = self.permissoes.orgao_selecionado

        self.assertEqual(orgao_selecionado, self.expected[0])

    def test_erro_se_usuario_nao_possuir_orgaos_validos(self):
        self.mock_oracle_access.side_effect = [
            (self.oracle_return_lista_orgao[1],),  # Apenas órgão inválido
            [],
            self.oracle_return_dados_usuario,
        ]
        with pytest.raises(exceptions.UserHasNoValidOfficesError):
            self.permissoes.orgaos_validos


class TestRetrieveDadosUsuario(TestCase):
    def setUp(self):
        self.username = "username"
        self.oracle_access_patcher = mock.patch(
            "dominio.login.dao.oracle_access"
        )
        self.mock_oracle_access = self.oracle_access_patcher.start()
        self.oracle_return_dados_usuario = (
            ("12345", "123456789", "NOME FUNCIONARIO", "X", "4567"),
        )
        self.mock_oracle_access.return_value = self.oracle_return_dados_usuario
        self.permissoes = services.PermissoesUsuarioRegular(
            username=self.username
        )

    def test_organiza_dados_do_usuario(self):
        dados = self.permissoes.dados_usuario
        expected = {
            "cpf": "123456789",
            "pess_dk": "4567",
            "nome": "NOME FUNCIONARIO",
            "matricula": "12345",
            "sexo": "X",
        }

        self.assertEqual(dados, expected)


class TestPermissoesRouter(TestCase):
    "Define qual controle de permissoes será usado"

    def setUp(self):
        self.json_master_1 = {
            "userDetails": {"login": "username"},
            "permissions": {
                "ROLE_qualquer": True,
                "ROLE_master": True,
            },  # possui ROLE especial
        }
        self.json_master_2 = {
            "userDetails": {"login": "username"},
            "permissions": {
                "ROLE_qualquer": True,
                "ROLE_especial": True,
            },  # possui ROLE especial
        }
        self.json_regular = {
            "userDetails": {"login": "username"},
            "permissions": {
                "ROLE_qualquer": True
            },  # não possuei ROLE especial
        }

    @override_settings(DOMINIO_ESPECIAL_ROLES=["ROLE_especial", "ROLE_master"])
    def test_role_router(self):
        permissao_especial_1 = services.permissoes_router(self.json_master_1)
        permissao_especial_2 = services.permissoes_router(self.json_master_2)
        permissao_regular = services.permissoes_router(self.json_regular)

        self.assertTrue(
            isinstance(permissao_especial_1, services.PermissoesUsuarioAdmin)
        )
        self.assertTrue(
            isinstance(permissao_especial_2, services.PermissoesUsuarioAdmin)
        )
        self.assertTrue(
            isinstance(permissao_regular, services.PermissoesUsuarioRegular)
        )

    def test_set_username_to_lower(self):
        self.json_regular["userDetails"]["info"] = "USERNAME"
        permissao = services.permissoes_router(self.json_regular)

        self.assertEqual(permissao.username, "username")


class TesPermissoesUsuarioAdmin(TestCase):
    def setUp(self):
        self.username = "username"
        self.oracle_access_patcher = mock.patch(
            "dominio.login.dao.oracle_access"
        )
        self.mock_oracle_access = self.oracle_access_patcher.start()
        self.oracle_return_dados_usuario = (
            ("12345", "123456789", "NOME FUNCIONARIO", "X", "4567"),
        )
        self.oracle_return_lista_todos_orgaos = (
            (
                "cdorgao 1",
                "PROMOTORIA INVESTIGAÇÃO PENAL",
                "matricula 1",
                "cpf 1",
                "nome 1",
                "X",
                "pess_dk 1",
            ),
            (
                "cdorgao 2",
                "PROMOTORIA DIFERENTE",
                "matricula 2",
                "cpf 2",
                "nome 2",
                "X",
                "pess_dk 2",
            ),
            (
                "cdorgao 3",
                "PROMOTORIA TUTELA COLETIVA",
                "matricula 3",
                "cpf 3",
                "nome 3",
                "X",
                "pess_dk 3",
            ),
        )
        self.mock_oracle_access.side_effect = [
            self.oracle_return_lista_todos_orgaos,
            self.oracle_return_dados_usuario,
        ]
        self.expected = [
            {
                "cpf": "cpf 1",
                "pess_dk": "pess_dk 1",
                "nome": "nome 1",
                "matricula": "matricula 1",
                "sexo": "X",
                "cdorgao": "cdorgao 1",
                "nm_org": "PROMOTORIA INVESTIGAÇÃO PENAL",
                "tipo": 2,
            },
            {
                "cpf": "cpf 2",
                "pess_dk": "pess_dk 2",
                "nome": "nome 2",
                "matricula": "matricula 2",
                "sexo": "X",
                "cdorgao": "cdorgao 2",
                "nm_org": "PROMOTORIA DIFERENTE",
                "tipo": 0,
            },
            {
                "cpf": "cpf 3",
                "pess_dk": "pess_dk 3",
                "nome": "nome 3",
                "matricula": "matricula 3",
                "sexo": "X",
                "cdorgao": "cdorgao 3",
                "nm_org": "PROMOTORIA TUTELA COLETIVA",
                "tipo": 1,
            },
        ]
        self.permissoes = services.PermissoesUsuarioAdmin(
            username=self.username
        )

    def test_retorna_todos_orgaos_lotados(self):
        orgaos = self.permissoes.orgaos_lotados

        self.assertEqual(orgaos, self.expected)

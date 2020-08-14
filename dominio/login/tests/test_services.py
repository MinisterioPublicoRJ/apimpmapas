from datetime import date
from unittest import mock

import pytest
from django.test import TestCase, override_settings
from freezegun import freeze_time
from model_bakery import baker

from dominio.login import services, exceptions
from dominio.login.dao import PIPValidasDAO, ListaDPsPIPsDAO
from dominio.models import Usuario


class TestBuildLoginResponse(TestCase):
    def setUp(self):
        self.TEST_DATABASE_NAME = "default"
        self.username = "username"

        self.pip_validos_dao_patcher = mock.patch.object(
            PIPValidasDAO,
            "execute"
        )
        self.pip_validos_mock = self.pip_validos_dao_patcher.start()
        # ids de pips validas
        self.pip_validos_mock.return_value = (("098765",),)

        self.pip_cisps_dao_patcher = mock.patch.object(
            ListaDPsPIPsDAO,
            "execute"
        )
        self.pip_cisps_mock = self.pip_cisps_dao_patcher.start()
        self.pip_cisps_mock.return_value = [("098765", "1,2,3"),]

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
                (
                    "098765",
                    "PROMOTORIA INVESTIGAÇÃO PENAL",
                    "MATRICULA 1",
                    "CPF 1",
                    "NOME 1",
                    "X",
                    "PESS_DK 1",
                ),
                (
                    "1234",
                    "PROMOTORIA DIFERENTE",
                    "MATRICULA 2",
                    "CPF 2",
                    "NOME 2",
                    "X",
                    "PESS_DK 2",
                ),
            ),
            (
                (
                    "1234",
                    "PROMOTORIA TUTELA COLETIVA",
                    "MATRICULA 3",
                    "CPF 3",
                    "NOME 3",
                    "X",
                    "PESS_DK 3",
                ),
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
            "tipo_permissao": "regular",
            "orgao_selecionado":
            {
                "cpf": "CPF 1",
                "matricula": "MATRICULA 1",
                "pess_dk": "PESS_DK 1",
                "nome": "NOME 1",
                "sexo": "X",
                "nm_org": "PROMOTORIA INVESTIGAÇÃO PENAL",
                "tipo": 2,
                "cdorgao": "098765",
                "dps": "1,2,3"
            },
            "orgaos_lotados": [
                {
                    "cpf": "CPF 1",
                    "matricula": "MATRICULA 1",
                    "pess_dk": "PESS_DK 1",
                    "nome": "NOME 1",
                    "sexo": "X",
                    "nm_org": "PROMOTORIA INVESTIGAÇÃO PENAL",
                    "tipo": 2,
                    "cdorgao": "098765",
                    "dps": "1,2,3"
                },
                {
                    "cpf": "CPF 2",
                    "matricula": "MATRICULA 2",
                    "pess_dk": "PESS_DK 2",
                    "nome": "NOME 2",
                    "sexo": "X",
                    "nm_org": "PROMOTORIA DIFERENTE",
                    "tipo": 0,
                    "cdorgao": "1234",
                    "dps": ""
                },
                {
                    "cpf": "CPF 3",
                    "matricula": "MATRICULA 3",
                    "pess_dk": "PESS_DK 3",
                    "nome": "NOME 3",
                    "sexo": "X",
                    "nm_org": "PROMOTORIA TUTELA COLETIVA",
                    "tipo": 1,
                    "cdorgao": "1234",
                    "dps": ""
                },
            ],
            "orgaos_validos": [
                {
                    "cpf": "CPF 1",
                    "matricula": "MATRICULA 1",
                    "pess_dk": "PESS_DK 1",
                    "nome": "NOME 1",
                    "sexo": "X",
                    "nm_org": "PROMOTORIA INVESTIGAÇÃO PENAL",
                    "tipo": 2,
                    "cdorgao": "098765",
                    "dps": "1,2,3"
                },
                {
                    "cpf": "CPF 3",
                    "matricula": "MATRICULA 3",
                    "pess_dk": "PESS_DK 3",
                    "nome": "NOME 3",
                    "sexo": "X",
                    "nm_org": "PROMOTORIA TUTELA COLETIVA",
                    "tipo": 1,
                    "cdorgao": "1234",
                    "dps": ""
                },
            ],
        }
        self.username = "username"
        self.permissoes = services.PermissoesUsuarioRegular(
            username=self.username
        )

    def tearDown(self):
        self.pip_validos_dao_patcher.stop()
        self.pip_cisps_dao_patcher.stop()
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

        self.pip_validos_dao_patcher = mock.patch.object(
            PIPValidasDAO,
            "execute"
        )
        self.pip_validos_mock = self.pip_validos_dao_patcher.start()
        # ids de pips validas
        self.pip_validos_mock.return_value = (("098765",),)

        self.pip_cisps_dao_patcher = mock.patch.object(
            ListaDPsPIPsDAO,
            "execute"
        )
        self.pip_cisps_mock = self.pip_cisps_dao_patcher.start()
        self.pip_cisps_mock.return_value = [("098765", "1,2,3"),]

        self.oracle_access_patcher = mock.patch(
            "dominio.login.dao.oracle_access"
        )
        self.mock_oracle_access = self.oracle_access_patcher.start()
        self.oracle_return_dados_usuario = (
            ("12345", "123456789", "NOME FUNCIONARIO", "X", "4567"),
        )
        self.oracle_return_lista_orgao = (
            (
                "098765",
                "PROMOTORIA INVESTIGAÇÃO PENAL",
                "MATRICULA 1",
                "CPF 1",
                "NOME 1",
                "X",
                "PESS_DK 1",

            ),
            (
                "1234",
                "PROMOTORIA DIFERENTE",
                "MATRICULA 2",
                "CPF 2",
                "NOME 2",
                "X",
                "PESS_DK 2",
            ),
        )
        self.oracle_return_lista_orgao_pessoal = (
            (
                "9999",
                "PROMOTORIA TUTELA COLETIVA",
                "MATRICULA 3",
                "CPF 3",
                "NOME 3",
                "X",
                "PESS_DK 3",
            ),
        )
        self.mock_oracle_access.side_effect = [
            self.oracle_return_lista_orgao,
            self.oracle_return_lista_orgao_pessoal,
            self.oracle_return_dados_usuario,
        ]
        self.expected = [
            {
                "cpf": "CPF 1",
                "pess_dk": "PESS_DK 1",
                "nome": "NOME 1",
                "matricula": "MATRICULA 1",
                "sexo": "X",
                "cdorgao": "098765",
                "nm_org": "PROMOTORIA INVESTIGAÇÃO PENAL",
                "tipo": 2,
                "dps": "1,2,3"
            },
            {
                "cpf": "CPF 2",
                "pess_dk": "PESS_DK 2",
                "nome": "NOME 2",
                "matricula": "MATRICULA 2",
                "sexo": "X",
                "cdorgao": "1234",
                "nm_org": "PROMOTORIA DIFERENTE",
                "tipo": 0,
                "dps": ""
            },
            {
                "cpf": "CPF 3",
                "pess_dk": "PESS_DK 3",
                "nome": "NOME 3",
                "matricula": "MATRICULA 3",
                "sexo": "X",
                "cdorgao": "9999",
                "nm_org": "PROMOTORIA TUTELA COLETIVA",
                "tipo": 1,
                "dps": ""
            },
        ]
        self.permissoes = services.PermissoesUsuarioRegular(
            username=self.username
        )

    def tearDown(self):
        self.oracle_access_patcher.stop()
        self.pip_validos_dao_patcher.stop()
        self.pip_cisps_dao_patcher.stop()

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

    def test_adiciona_cisps(self):
        lista_orgaos = self.expected.copy()
        del lista_orgaos[0]['dps']
        del lista_orgaos[1]['dps']
        del lista_orgaos[2]['dps']
        cisps_promotorias = self.permissoes._adiciona_cisps(lista_orgaos)

        self.assertEqual(cisps_promotorias, self.expected)

    def test_pip_cisps(self):
        response = self.permissoes.pip_cisps()
        expected = {"098765": "1,2,3"}
        self.assertEqual(response, expected)

    def test_get_cisps_from_orgao(self):
        id_orgao = "098765"
        expected = "1,2,3"
        response = self.permissoes._get_cisps_from_orgao(id_orgao)
        self.assertEqual(response, expected)

        id_orgao = "1234"
        expected = ""
        response = self.permissoes._get_cisps_from_orgao(id_orgao)
        self.assertEqual(response, expected)

    def test_filtra_pip_invalida(self):
        self.pip_validos_mock.return_value = (("another id",),)

        lista_orgaos = self.permissoes.orgaos_validos
        self.expected = [self.expected[2]]

        self.assertEqual(lista_orgaos, self.expected)

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
        self.pip_validos_dao_patcher = mock.patch.object(
            PIPValidasDAO,
            "execute"
        )
        self.pip_validos_mock = self.pip_validos_dao_patcher.start()
        # ids de pips validas
        self.pip_validos_mock.return_value = (("cdorgao 1",),)

        self.pip_cisps_dao_patcher = mock.patch.object(
            ListaDPsPIPsDAO,
            "execute"
        )
        self.pip_cisps_mock = self.pip_cisps_dao_patcher.start()
        self.pip_cisps_mock.return_value = [("cdorgao 1", "1,2,3"), ("cdorgao 4", "1,2,3")]

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
            # Essa PIP deve ser removida por não estar na lista pip_validas
            (
                "cdorgao 4",
                "PROMOTORIA INVESTIGAÇÃO PENAL",
                "matricula 4",
                "cpf 4",
                "nome 4",
                "X",
                "pess_dk 4",
            ),
        )
        self.oracle_return_lista_orgaos_lotados = (
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
                "cdorgao 5",
                "PROMOTORIA TUTELA COLETIVA",
                "matricula 5",
                "cpf 5",
                "nome 5",
                "X",
                "pess_dk 5",
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
                "dps": "1,2,3"
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
                "dps": ""
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
                "dps": ""
            },
            {
                "cpf": "cpf 4",
                "pess_dk": "pess_dk 4",
                "nome": "nome 4",
                "matricula": "matricula 4",
                "sexo": "X",
                "cdorgao": "cdorgao 4",
                "nm_org": "PROMOTORIA INVESTIGAÇÃO PENAL",
                "tipo": 2,
                "dps": "1,2,3"
            },
        ]
        self.permissoes = services.PermissoesUsuarioAdmin(
            username=self.username
        )

    def tearDown(self):
        self.pip_validos_dao_patcher.stop()
        self.oracle_access_patcher.stop()
        self.pip_cisps_dao_patcher.stop()

    def test_retorna_todos_orgaos(self):
        orgaos = self.permissoes.todos_orgaos

        self.assertEqual(orgaos, self.expected)

    def test_retorna_todos_orgaos_validos(self):
        self.mock_oracle_access.side_effect = [
            self.oracle_return_lista_todos_orgaos,
        ]
        orgaos = self.permissoes.orgaos_validos
        self.expected.pop(1)  # Removido pelo filtro tipo_orgao
        self.expected.pop(-1)  # Removido pelo filtro pip_validas

        self.assertCountEqual(orgaos, self.expected)

    def test_filtra_pip_invalida(self):
        self.pip_validos_mock.return_value = (("cdorgao 4",),)

        lista_orgaos = self.permissoes.orgaos_validos
        self.expected = self.expected[2:4]

        self.assertEqual(lista_orgaos, self.expected)

    def test_orgao_selecionado_permissao_admin_seleciona_lotado(self):
        "Deve tentar selecionar primeiro um orgao lotado valido"
        self.mock_oracle_access.side_effect = [
            self.oracle_return_lista_orgaos_lotados,
            (),
            self.oracle_return_lista_todos_orgaos,
        ]
        expected = {
                "cpf": "cpf 5",
                "pess_dk": "pess_dk 5",
                "nome": "nome 5",
                "matricula": "matricula 5",
                "sexo": "X",
                "cdorgao": "cdorgao 5",
                "nm_org": "PROMOTORIA TUTELA COLETIVA",
                "tipo": 1,
                "dps": ""
            }

        orgao_selecionado = self.permissoes.orgao_selecionado

        self.assertEqual(orgao_selecionado, expected)

    def test_orgao_selecionado_permissao_admin_seleciona_primeiro_lista(self):
        "Deve tentar selecionar primeiro um orgao lotado valido"
        self.mock_oracle_access.side_effect = [
            ((
                "cdorgao 2",
                "PROMOTORIA DIFERENTE",
                "matricula 2",
                "cpf 2",
                "nome 2",
                "X",
                "pess_dk 2",
            ),),
            (),
            self.oracle_return_lista_todos_orgaos,
        ]

        orgao_selecionado = self.permissoes.orgao_selecionado

        self.assertEqual(orgao_selecionado, self.expected[0])

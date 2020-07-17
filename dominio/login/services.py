from collections import namedtuple

import logging
import jwt
from cached_property import cached_property
from django.conf import settings

from dominio.exceptions import APIEmptyResultError
from dominio.models import Usuario
from dominio.login import dao, exceptions
from login.jwtlogin import tipo_orgao


login_logger = logging.getLogger(__name__)


# deveria ser abstrata?
class PermissaoUsuario:
    def __init__(self, username):
        self._username = username

    @property
    def username(self):
        return self._username

    @cached_property
    def orgaos_lotados(self):
        lista_orgaos = []
        for permissao in self.permissoes_dao:
            try:
                orgaos = permissao.handler.get(
                    login=self._username, **permissao.kwargs
                )
            except APIEmptyResultError:
                raise exceptions.UserHasNoOfficeInformation

            lista_orgaos.extend(orgaos)

        lista_orgaos = self._classifica_orgaos(lista_orgaos)
        return self._preenche_dados_usuario(lista_orgaos)

    @cached_property
    def orgaos_validos(self):
        lista_orgaos_validos = self._filtra_orgaos_invalidos(
            self.orgaos_lotados
        )
        if not lista_orgaos_validos:
            raise exceptions.UserHasNoValidOfficesError

        return lista_orgaos_validos

    @property
    def orgao_selecionado(self):
        "Até o momento o primeiro órgão válido é selecionado"
        return self.orgaos_validos[0]

    @cached_property
    def dados_usuario(self):
        try:
            dados = dao.DadosUsuarioDAO.get(login=self.username)
        except APIEmptyResultError:
            raise exceptions.UserDetailsNotFoundError

        return dados

    def _classifica_orgaos(self, lista_orgaos):
        lista_orgaos_copy = lista_orgaos.copy()
        for orgao in lista_orgaos_copy:
            orgao["tipo"] = tipo_orgao(orgao["nm_org"])

        return lista_orgaos_copy

    def _preenche_dados_usuario(self, orgaos):
        orgaos_copy = orgaos.copy()
        for orgao in orgaos_copy:
            orgao.update(self.dados_usuario)

        return orgaos_copy

    def _filtra_orgaos_invalidos(self, lista_orgaos):
        return [orgao for orgao in lista_orgaos if orgao["tipo"] != 0]


class PermissoesUsuarioRegular(PermissaoUsuario):
    DaoWrapper = namedtuple("PermissaoDao", ["handler", "kwargs"])
    permissoes_dao = [
        DaoWrapper(dao.ListaOrgaosDAO, {"accept_empty": False}),
        DaoWrapper(dao.ListaOrgaosPessoalDAO, {"accept_empty": True}),
    ]


class PermissoesUsuarioAdmin(PermissaoUsuario):
    DaoWrapper = namedtuple("PermissaoDao", ["handler", "kwargs"])
    permissoes_dao = [
        DaoWrapper(dao.ListaTodosOrgaosDAO, {"accept_empty": False}),
    ]

    def __init__(self, username):
        self._username = username

    # Refatorar para não repetir este método
    @cached_property
    def orgaos_lotados(self):
        lista_orgaos = []
        for permissao in self.permissoes_dao:
            lista_orgaos.extend(permissao.handler.get(**permissao.kwargs))

        lista_orgaos = self._classifica_orgaos(lista_orgaos)
        return self._preenche_dados_usuario(lista_orgaos)

    def _preenche_dados_usuario(self, orgaos):
        return orgaos


def permissoes_router(info):
    username = info["userDetails"]["login"].lower()
    # TODO: se número de permissoes crescrer utilizar estratégia mais SOLID
    cls_permissoes = PermissoesUsuarioRegular
    if any(
        [
            info["permissions"].get(role, False)
            for role in settings.DOMINIO_ESPECIAL_ROLES
        ]
    ):
        cls_permissoes = PermissoesUsuarioAdmin

    return cls_permissoes(username)


def build_login_response(permissoes):
    usuario, created = Usuario.objects.get_or_create(
        username=permissoes.username
    )

    response = dict()
    # Informações do login
    response["username"] = usuario.username
    response["first_login"] = created
    response["first_login_today"] = created or usuario.get_first_login_today()

    # Informações do usuário
    response["sexo"] = permissoes.dados_usuario["sexo"]
    response["pess_dk"] = permissoes.dados_usuario["pess_dk"]
    response["cpf"] = permissoes.dados_usuario["cpf"]
    response["nome"] = permissoes.dados_usuario["nome"]
    response["matricula"] = permissoes.dados_usuario["matricula"]

    response["token"] = jwt.encode(
        response, settings.JWT_SECRET, algorithm="HS256",
    )

    # Informações do órgao seecionado
    response["tipo_orgao"] = permissoes.orgao_selecionado["tipo"]
    response["orgao"] = permissoes.orgao_selecionado["cdorgao"]
    response["orgaos_validos"] = permissoes.orgaos_validos

    # Update last_login
    usuario.save()

    return response
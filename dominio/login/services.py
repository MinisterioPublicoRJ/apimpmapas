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


class PermissoesUsuarioPromotron:
    DaoWrapper = namedtuple("PermissaoDao", ["handler", "kwargs"])
    permissoes_dao = [
        DaoWrapper(dao.ListaOrgaosDAO, {"accept_empty": False}),
        DaoWrapper(dao.ListaOrgaosPessoalDAO, {"accept_empty": True}),
    ]
    user_info_fields = ["cpf", "matricula", "nome", "pess_dk", "sexo"]

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
        return lista_orgaos

    @cached_property
    def orgaos_validos(self):
        lista_orgaos_validos = self._filtra_orgaos_invalidos(
            self.orgaos_lotados
        )
        if not lista_orgaos_validos:
            raise exceptions.UserHasNoValidOfficesError

        return lista_orgaos_validos

    @cached_property
    def dados_usuario(self):
        dados = {}
        for orgao in self.orgaos_validos:
            # Checa se retorno do banco possui todos os dados do usuário
            if not set(self.user_info_fields) - set(orgao.keys()):
                for field in self.user_info_fields:
                    dados[field] = orgao[field]

        if not dados:
            raise exceptions.UserDetailsNotFoundError

        return dados

    @property
    def orgao_selecionado(self):
        "Até o momento o primeiro órgão válido é selecionado"
        return self.orgaos_validos[0]

    def _classifica_orgaos(self, lista_orgaos):
        lista_orgaos_copy = lista_orgaos.copy()
        for orgao in lista_orgaos_copy:
            orgao["tipo"] = tipo_orgao(orgao["nm_org"])

        return lista_orgaos_copy

    def _filtra_orgaos_invalidos(self, lista_orgaos):
        return [orgao for orgao in lista_orgaos if orgao["tipo"] != 0]


class PermissaoEspecialPromotron:
    def __init__(self, username):
        self._username = username


def permissoes_router(info):
    username = info["userDetails"]["login"].lower()
    #TODO: se número de permissoes crescrer utilizar estratégia mais SOLID
    cls_permissoes = PermissoesUsuarioPromotron
    if any(
        [
            info["permissions"].get(role, False)
            for role in settings.DOMINIO_ESPECIAL_ROLES
        ]
    ):
        cls_permissoes = PermissaoEspecialPromotron

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

    # Informações do órgao seecionado
    response["tipo_orgao"] = permissoes.orgao_selecionado["tipo"]
    response["orgao"] = permissoes.orgao_selecionado["cdorgao"]
    response["orgaos_validos"] = permissoes.orgaos_validos

    response["token"] = jwt.encode(
        response, settings.JWT_SECRET, algorithm="HS256",
    )

    # Update last_login
    usuario.save()

    return response

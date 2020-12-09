from collections import namedtuple

import logging
import jwt
from cached_property import cached_property
from django.conf import settings

from dominio.exceptions import APIEmptyResultError
from dominio.models import Usuario
from dominio.login import dao, exceptions
from dominio.login.exceptions import UserHasNoValidOfficesError
from login.jwtlogin import tipo_orgao


login_logger = logging.getLogger(__name__)
DAO_WRAPPER = namedtuple("PermissaoDao", ["handler", "kwargs"])


# deveria ser abstrata?
class PermissaoUsuario:
    cd_pips_especializadas = (
        "29941099",
        "29941140",
        "29941222",
        "29941251",
        "29941368",
        "30061803",
        "30070783",
        "30070806",
    )

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
        lista_orgaos = self._adiciona_cisps(lista_orgaos)
        lista_orgaos = self._classifica_pips_especializadas(lista_orgaos)
        return lista_orgaos

    @cached_property
    def atribuicoes_orgaos(self):
        ids_orgaos_lotados = [
            int(o.get("cdorgao")) for o in self.orgaos_lotados
        ]
        return dao.AtribuicoesOrgaosDAO.get(
            ids_orgaos=ids_orgaos_lotados,
            accept_empty=True
        ).get("atribuicao")

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

    def _filtra_orgaos_invalidos(self, lista_orgaos):
        validos = [orgao for orgao in lista_orgaos if orgao["tipo"] != 0]
        return [
            orgao for orgao in validos if "TUTELA" in orgao["nm_org"]
            or orgao["cdorgao"] in self.pip_validas
        ]

    def _adiciona_cisps(self, lista_orgaos):
        lista_orgaos_copy = lista_orgaos.copy()
        for orgao in lista_orgaos_copy:
            orgao["dps"] = self._get_cisps_from_orgao(orgao["cdorgao"])

        return lista_orgaos_copy

    def _classifica_pips_especializadas(self, lista_orgaos):
        for orgao in lista_orgaos:
            orgao["pip_especializada"] = None
            if (
                orgao["cdorgao"] in self.pip_validas
                and orgao["cdorgao"] in self.cd_pips_especializadas
            ):
                orgao["pip_especializada"] = True
            elif orgao["cdorgao"] in self.pip_validas:
                orgao["pip_especializada"] = False

        return lista_orgaos

    @cached_property
    def pip_validas(self):
        return [r["id_orgao"] for r in dao.PIPValidasDAO.get()]

    @cached_property
    def pip_cisps(self):
        lista_cisps = dao.ListaDPsPIPsDAO.get()
        return {d['id_orgao']: d['dps'] for d in lista_cisps}

    @property
    def ids_orgaos_lotados_validos(self):
        return [o.get("cdorgao") for o in self.orgaos_validos]

    def _get_cisps_from_orgao(self, id_orgao):
        return self.pip_cisps.get(id_orgao, '')


class PermissoesUsuarioRegular(PermissaoUsuario):
    type = "regular"
    permissoes_dao = [
        DAO_WRAPPER(dao.ListaOrgaosDAO, {"accept_empty": False}),
    ]


class PermissoesUsuarioAdmin(PermissaoUsuario):
    type = "admin"
    permissoes_dao = [
        DAO_WRAPPER(dao.ListaOrgaosDAO, {"accept_empty": True}),
    ]

    def __init__(self, username):
        self._username = username

    @cached_property
    def todos_orgaos(self):
        lista_orgaos = dao.ListaTodosOrgaosDAO.get()
        lista_orgaos = self._classifica_orgaos(lista_orgaos)
        lista_orgaos = self._adiciona_cisps(lista_orgaos)
        return self._classifica_pips_especializadas(lista_orgaos)

    @property
    def orgaos_validos(self):
        return self._filtra_orgaos_invalidos(self.todos_orgaos)

    @property
    def orgao_selecionado(self):
        lotados_validos = self._filtra_orgaos_invalidos(self.orgaos_lotados)
        return (
            lotados_validos[0] if lotados_validos else self.orgaos_validos[0]
        )


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
    response = dict()

    # Informações do usuário
    response["sexo"] = permissoes.dados_usuario["sexo"]
    response["pess_dk"] = permissoes.dados_usuario["pess_dk"]
    response["cpf"] = permissoes.dados_usuario["cpf"]
    response["nome"] = permissoes.dados_usuario["nome"]
    response["matricula"] = permissoes.dados_usuario["matricula"]
    response["tipo_permissao"] = permissoes.type
    response["atribuicao"] = permissoes.atribuicoes_orgaos

    try:
        response["ids_orgaos_lotados_validos"] = (
            permissoes.ids_orgaos_lotados_validos
        )
        usuario, created = Usuario.objects.get_or_create(
            username=permissoes.username
        )

        # Informações do login
        response["username"] = permissoes.username
        response["first_login"] = created
        response["first_login_today"] = (
            created or usuario.get_first_login_today()
        )
        token = jwt.encode(
            response, settings.JWT_SECRET, algorithm="HS256",
        )

        # Informações dos órgãos
        response["orgaos_lotados"] = permissoes.orgaos_lotados
        response["orgao_selecionado"] = permissoes.orgao_selecionado
        response["orgaos_validos"] = permissoes.orgaos_validos

        # Token de acesso
        response["token"] = token

        # Update last_login
        usuario.save()
    except UserHasNoValidOfficesError:
        response["orgao_selecionado"] = None
        response["orgaos_validos"] = None
        response["ids_orgaos_lotados_validos"] = None

    return response

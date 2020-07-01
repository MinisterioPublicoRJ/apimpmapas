from collections import namedtuple

import logging
import jwt
from django.conf import settings

from dominio import exceptions
from dominio.models import Usuario
from dominio.login import dao
from login.jwtlogin import tipo_orgao


login_logger = logging.getLogger(__name__)


class PermissoesUsuarioPromotron:
    DaoWrapper = namedtuple("PermissaoDao", ["handler", "kwargs"])
    permissoes_dao = [
        DaoWrapper(dao.ListaOrgaosDAO, {"accept_empty": False}),
        DaoWrapper(dao.ListaOrgaosPessoalDAO, {"accept_empty": True}),
    ]

    @classmethod
    def get_orgaos_lotados(cls, **kwargs):
        lista_orgaos = []
        for permissao in cls.permissoes_dao:
            lista_orgaos.extend(
                permissao.handler.get(**{**kwargs, **permissao.kwargs})
            )

        return lista_orgaos


def build_login_response(username):
    usuario, created = Usuario.objects.get_or_create(
        username=username
    )

    try:
        lista_orgaos = PermissoesUsuarioPromotron.get_orgaos_lotados(
            login=username
        )
    except exceptions.APIEmptyResultError:
        raise exceptions.UserHasNoValidOfficesError

    orgaos_validos = filtra_orgaos_validos(
        classifica_orgaos(lista_orgaos)
    )
    if not orgaos_validos:
        logging.info("Nenhum órgão válido encontrado para '{username}'")
        raise exceptions.UserHasNoValidOfficesError

    response = dict()
    response["orgao"] = orgaos_validos[0]["cdorgao"]
    response["username"] = usuario.username
    response["first_login"] = created
    response["first_login_today"] = (
        created or usuario.get_first_login_today()
    )
    response["sexo"] = lista_orgaos[0]["sexo"]
    response["pess_dk"] = lista_orgaos[0]["pess_dk"]
    response["cpf"] = lista_orgaos[0]["cpf"]
    response["nome"] = lista_orgaos[0]["nome"]
    response["tipo_orgao"] = orgaos_validos[0]["tipo"]
    response["matricula"] = lista_orgaos[0]["matricula"]

    response["orgaos_validos"] = orgaos_validos

    response["token"] = jwt.encode(
        response,
        settings.JWT_SECRET,
        algorithm="HS256",
    )

    # Update last_login
    usuario.save()

    return response


def classifica_orgaos(lista_orgaos):
    return [
        {
            "orgao": orgao["nm_org"],
            "tipo": tipo_orgao(orgao["nm_org"]),
            "cdorgao": orgao["cdorgao"],
        }
        for orgao in lista_orgaos
    ]


def filtra_orgaos_validos(lista_orgaos):
    return [orgao for orgao in lista_orgaos if orgao["tipo"] != 0]

import logging
import jwt
from django.conf import settings

from login.jwtlogin import get_jwt_from_post, tipo_orgao
from dominio.login.dao import DPsPIPDAO


login_logger = logging.getLogger(__name__)


def authenticate_integra(request):
    token_part = get_jwt_from_post(request)
    payload = jwt.decode(token_part, verify=False)
    login_logger.info(
        f"Login efetuado pelo órgão ->"
        f" {payload['scaUser'].get('nomeOrgaoUsuario', '-')}"
        f" : {payload['scaUser'].get('nomeOrgao', '-')}"
        f" : {payload['scaUser'].get('orgaoUsuario', '-')}"
    )

    user_name = payload['user_name']
    cpf = payload['scaUser']['cpfUsuario']
    orgao = payload['scaUser']['orgao']
    pess_dk = payload['scaUser']['pessDK']
    nome_usuario = payload['scaUser']['nomeUsuario']
    nome_orgao = payload['scaUser']['nomeOrgaoUsuario']
    matricula = payload["scaUser"]["matricula"]

    dps = DPsPIPDAO.get(accept_empty=True, orgao=int(orgao)).get('dps', '')

    payload = {
        'username': user_name,
        'cpf': cpf,
        'orgao': orgao,
        'pess_dk': pess_dk,
        'nome': nome_usuario,
        'tipo_orgao': tipo_orgao(nome_orgao),
        'matricula': matricula,
        'dps': dps
    }

    token = jwt.encode(
        payload,
        settings.JWT_SECRET,
        algorithm='HS256'
    )

    payload = {**payload, **{"token": token.decode("latin-1")}}

    return payload

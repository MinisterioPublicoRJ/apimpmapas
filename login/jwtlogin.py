import jwt
from django.conf import settings


def authenticate_integra(request):
    token_part = request.headers['AUTHORIZATION']
    token_part = token_part.split(' ')[1]
    payload = jwt.decode(token_part, verify=False)

    user_name = payload['user_name']
    cpf = payload['scaUser']['cpfUsuario']
    orgao = payload['scaUser']['orgao']
    pess_dk = payload['scaUser']['pessDK']
    nome_usuario = payload['scaUser']['nomeUsuario']

    payload = {
        'username': user_name,
        'cpf': cpf,
        'orgao': orgao,
        'pess_dk': pess_dk,
        'nome': nome_usuario
    }

    token = jwt.encode(
        payload,
        settings.JWT_SECRET,
        algorithm='HS256'
    )

    payload['token'] = token.decode('latin1')

    return payload

import jwt
from django.conf import settings


def get_jwt_from_post(request):
    token_part = request.POST['jwt']
    return token_part


def get_jwt_from_get(request):
    token_part = request.GET['jwt']
    return token_part


def authenticate_integra(request):
    token_part = get_jwt_from_post(request)
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

    payload = {**payload, **{"token": token.decode("latin-1")}}

    return payload


def unpack_jwt(request):
    token = get_jwt_from_get(request)
    return jwt.decode(
        token,
        settings.JWT_SECRET,
        algorithm='HS256'
    )

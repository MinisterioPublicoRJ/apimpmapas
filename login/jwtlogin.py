import jwt
from django.conf import settings


def get_jwt_from_post(request):
    token_part = request.POST['jwt']
    return token_part


def get_jwt_from_get(request):
    token_part = request.GET['jwt']
    return token_part


def tipo_orgao(nome_orgao):
    nome_orgao = nome_orgao.lower()
    return int("tutela" in nome_orgao
               and not ("idoso" in nome_orgao or "infância" in nome_orgao))


def unpack_jwt(request):
    token = get_jwt_from_get(request)
    return jwt.decode(
        token,
        settings.JWT_SECRET,
        algorithm='HS256'
    )

import base64
import json
import requests

from django.conf import settings


def authenticate(username, password):
    password = bytes(password, 'utf-8')
    session = requests.session()

    response = session.post(
        url=settings.AUTH_MPRJ,
        data={
            'username': username,
            'password': base64.b64encode(password).decode('utf-8') 
        }
    )

    if response.status_code == 200:
        user_info = session.get(url=settings.AITJ_MPRJ_USERINFO)
        body = json.loads(user_info.content.decode('utf-8'))
        permissions = body['permissions']
        if (
            'ROLE_mp_plus_admin' in permissions
            and permissions['ROLE_mp_plus_admin']
        ):
            return response.status_code
    return 403

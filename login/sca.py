import base64
import json
import requests

from decouple import config


def authenticate(username, password):
    password = bytes(password, 'utf-8')
    session = requests.session()

    response = session.post(
        url=config('SCA_AUTH'),
        data={
            'username': username,
            'password': base64.b64encode(password).decode('utf-8')
        }
    )

    if response.status_code == 200:
        user_info = session.get(url=config('SCA_CHECK'))
        body = json.loads(user_info.content.decode('utf-8'))
        permissions = body['permissions']
        if (
            'ROLE_mp_plus_admin' in permissions
            and permissions['ROLE_mp_plus_admin']
        ):
            return response.status_code
    return 403

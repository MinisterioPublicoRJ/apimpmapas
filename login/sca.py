from decouple import config
from login_sca import login


def authenticate(username, password):
    password = bytes(password, 'utf-8')

    response = login(
        username,
        password,
        config('SCA_AUTH'),
        config('SCA_CHECK')
    )

    if response.auth.status_code == 200:
        login_info = response.info.json()
        permissions = login_info['permissions']
        if (
            'ROLE_mp_plus_admin' in permissions
            and permissions['ROLE_mp_plus_admin']
        ):
            return 200
    return 403

from django.conf import settings
from login_sca import login


# TODO: testar função `has_role`
def has_role(permissions, roles):
    return any([permissions.get(role, False) for role in roles])


def authenticate(username, password, roles=None, verify_roles=True):
    roles = roles or ('ROLE_mp_plus_admin',)
    password = bytes(password, 'utf-8')

    response = login(
        username,
        password,
        settings.SCA_AUTH,
        settings.SCA_CHECK
    )

    if response.auth.status_code == 200:
        login_info = response.info.json()
        permissions = login_info['permissions']
        if not verify_roles or has_role(permissions, roles):
            permission_list = []
            for permission, status in permissions.items():
                if status:
                    permission_list.append(permission)
            return {
                'logged_in': True,
                'permissions': permission_list
            }

    return {'logged_in': False}

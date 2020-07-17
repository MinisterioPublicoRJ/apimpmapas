from django.conf import settings

from rest_framework_simplejwt.tokens import AccessToken, RefreshToken


class TokenDoesNotHaveRoleException(Exception):
    pass


class SCAAccessTokenMixin:
    def __init__(self, username=None, token=None, verify=True):
        self._username = username

        super().__init__(token=token, verify=verify)
        if not token:
            self.set_roles()
            self.set_username()
        else:
            self.verify_role()

    def set_roles(self):
        self.payload["roles"] = (settings.PROXIES_PLACAS_ROLE,)

    def set_username(self):
        if self._username:
            self.payload["username"] = self._username

    def verify_role(self):
        if settings.PROXIES_PLACAS_ROLE not in self.payload.get("roles", []):
            raise TokenDoesNotHaveRoleException


class SCAAccessToken(SCAAccessTokenMixin, AccessToken):
    pass


class SCARefreshToken(SCAAccessTokenMixin, RefreshToken):
    pass

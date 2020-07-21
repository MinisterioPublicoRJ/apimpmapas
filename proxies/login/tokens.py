from rest_framework_simplejwt.tokens import RefreshToken


class SCAAccessToken(RefreshToken):
    def __init__(self, username=None, roles=None, token=None, verify=True):
        self._username = username
        self._roles = roles

        super().__init__(token=token, verify=verify)
        if not token:
            self.set_roles()
            self.set_username()

    def set_roles(self):
        self.payload["roles"] = self._roles

    def set_username(self):
        if self._username:
            self.payload["username"] = self._username

from django.conf import settings

from rest_framework_simplejwt.tokens import RefreshToken


class SCARefreshToken(RefreshToken):
    def __init__(self, token=None, verify=True):
        super().__init__(token=token, verify=verify)
        self.set_roles()

    def set_roles(self):
        self.payload["roles"] = (settings.PROXIES_PLACAS_ROLE,)

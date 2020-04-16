from django.core.cache import cache


class DataTrafficController:
    def __init__(self, rg):
        self.rg = rg

    @property
    def cache_key(self):
        return f"detran_request_line_{self.rg}"

    @property
    def request_awaiting(self):
        return cache.get(self.cache_key)

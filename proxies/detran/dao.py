from django.core.cache import cache


class DataTrafficController:
    def __init__(self, rg):
        self.rg = rg

    @property
    def cache_key(self):
        return f"detran_request_line_{self.rg}"

    def get_or_set_cache(self):
        return cache.get_or_set(self.cache_key, True)

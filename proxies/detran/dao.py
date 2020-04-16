from django.core.cache import cache

from proxies.detran.client import request_data as request_detran_data


class DataTrafficController:
    def __init__(self, rg):
        self.rg = rg

    @property
    def cache_key(self):
        return f"detran_request_line_{self.rg}"

    def get_or_set_cache(self):
        return cache.get_or_set(self.cache_key, True)

    def dispatch_request(self):
        return request_detran_data(self.rg)

    def get_data(self):
        """
        This method checks if a request was already sent to the service.
        If not it will dispatch a new request. Otherwise, it will wait and
        look for the data in the database.
        """
        request_sent = self.get_or_set_cache()
        if not request_sent:
            data = self.dispatch_request()

        return data

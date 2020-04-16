from time import sleep

from django.core.cache import cache

from proxies.detran.client import request_data as request_detran_data
from proxies.exceptions import WaitDBException


class DataTrafficController:
    def __init__(self, rg, wait_time=3, max_attempts=3):
        self.rg = rg
        self.wait_time = wait_time
        self.max_attempts = max_attempts

    @property
    def cache_key(self):
        return f"detran_request_line_{self.rg}"

    def get_or_set_cache(self):
        return cache.get_or_set(self.cache_key, True)

    def dispatch_request(self):
        data = request_detran_data(self.rg)
        cache.delete(self.cache_key)
        return data

    def persist_data(self, data):
        pass

    def get_db_data(self):
        pass

    def wait_for_data(self):
        sleep(self.wait_time)
        data = self.get_db_data()
        attempts = 1
        while not data and attempts < self.max_attempts:
            sleep(self.wait_time)
            data = self.get_db_data()
            attempts += 1

        if not data:
            raise WaitDBException("Tempo de espera pelos dados estourou o limite")

        return data

    def get_data(self):
        """
        This method checks if a request was already sent to the service.
        If not it will dispatch a new request. Otherwise, it will wait and
        look for the data in the database.
        """
        request_sent = self.get_or_set_cache()
        if not request_sent:
            data = self.dispatch_request()
            self.persist_data(data)
        else:
            data = self.wait_for_data()

        return data

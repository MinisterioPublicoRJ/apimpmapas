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
        # Se estourar excessao, preciso remover do cache
        # try, except, cache.delete, raise
        data = request_detran_data(self.rg)
        cache.delete(self.cache_key)
        return data

    def persist_photo(self, photo):
        pass

    def get_db_data(self):
        pass

    def get_db_photo(self):
        pass

    def wait_for_photo(self):
        sleep(self.wait_time)
        photo = self.get_db_photo()
        attempts = 1
        while not photo and attempts < self.max_attempts:
            sleep(self.wait_time)
            photo = self.get_db_photo()
            attempts += 1

        if not photo:
            raise WaitDBException(
                f"Tempo de espera pelos dados do {self.rg} estourou o limite"
            )

        return photo

    def get_photo(self):
        """
        This method checks if a request was already sent to the service.
        If not it will dispatch a new request. Otherwise, it will wait and
        look for the photo in the database.
        """
        request_sent = self.get_or_set_cache()
        if not request_sent:
            photo = self.dispatch_request()
            self.persist_photo(photo)
        else:
            photo = self.wait_for_photo()

        return photo


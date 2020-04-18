from time import sleep

from django.conf import settings
from django.core.cache import cache
from happybase import Connection as HBaseConnection

from dominio.db_connectors import execute as impala_execute
from proxies.detran.client import request_data as request_detran_data
from proxies.exceptions import DataDoesNotExistException, WaitDBException


class HBaseGate:
    def __init__(self, table_name, server=None, timeout=None):
        self.table_name = table_name
        self.server = server or settings.HBASE_SERVER
        self.timeout = timeout or settings.HBASE_TIMEOUT

    @property
    def get_table(self):
        try:
            connection = HBaseConnection(self.server, timeout=self.timeout)
        except:
            connection = HBaseConnection(self.server, timeout=self.timeout)

        return connection.table(self.table_name)

    def select(self, row_id, columns):
        return self.get_table.row(row_id, columns=columns)

    def insert(self, row_id, data):
        self.get_table.put(row_id, data=data)


class ImpalaGate:
    def __init__(self, table_name):
        self.table_name = table_name

    def select(self, columns, parameters):
        #TODO: criar um método genérico para formatar a query
        query = "SELECT {projection} FROM {table_name} WHERE {0} = :{0}"
        f_query = query.format(
            projection=", ".join(columns),
            table_name=self.table_name,
            *parameters.keys()
        )
        return impala_execute(f_query, parameters)


class DataTrafficController:
    def __init__(self, rg, wait_time=3, max_attempts=3):
        self.rg = rg
        self.wait_time = wait_time
        self.max_attempts = max_attempts
        self.hbase = HBaseGate(table_name=settings.HBASE_DETRAN_BASE)
        self.impala = ImpalaGate(table_name=settings.IMPALA_DETRAN_TABLE)

        # TODO: receber como argumento
        self.photo_column = "detran:foto"
        self.db_key = "rg"

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
        self.hbase.insert(row_id=self.rg, data={self.photo_column: photo})

    def get_db_data(self):
        return self.impala.select(
            columns=["*"],
            parameters={self.db_key: self.rg}
        )

    def get_db_photo(self):
        return self.hbase.select(row_id=self.rg, columns=[self.photo_column])

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

    def request_photo(self):
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

    def get_data(self):
        db_data = self.get_db_data()

        if not db_data:
            raise DataDoesNotExistException(
                f"Não existem dados para {self.rg}"
            )
        photo = self.get_db_photo()
        if not photo:
            photo = self.request_photo()

        db_data.update({"photo": photo})
        return db_data

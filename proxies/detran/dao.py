import logging
from hashlib import md5
from time import sleep

from django.conf import settings
from django.core.cache import cache
from happybase import Connection as HBaseConnection

from dominio.db_connectors import execute as impala_execute
from proxies.detran.client import request_data as request_detran_data
from proxies.detran.serializers import DetranSerializer
from proxies.exceptions import (
    DataDoesNotExistException,
    DetranAPIClientError,
    WaitDBException,
)

logger = logging.getLogger(__name__)


class HBaseGate:
    def __init__(self, table_name, server=None, timeout=None):
        self.table_name = table_name
        self.server = server or settings.HBASE_SERVER
        self.timeout = timeout or settings.HBASE_TIMEOUT

    @property
    def get_table(self):
        try:
            connection = HBaseConnection(self.server, timeout=self.timeout)
        except Exception:
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
        # TODO: criar um método genérico para formatar a query
        query = "SELECT {projection} FROM {table_name} WHERE {0} = :{0}"
        f_query = query.format(
            projection=", ".join(columns),
            table_name=self.table_name,
            *parameters.keys(),
        )
        return impala_execute(f_query, parameters)


class DataTrafficController:
    def __init__(
        self, rg, data_dao=None, photo_dao=None, wait_time=3, max_attempts=3
    ):
        self.rg = rg
        self.data_dao = data_dao
        self.photo_dao = photo_dao

        # TODO: receber como argumento
        self.serializer_obj = DetranSerializer

        self.wait_time = wait_time
        self.max_attempts = max_attempts

        # TODO: receber como argumento
        self.photo_column = "detran:foto"
        self.hash_column = "detran:foto_hash"
        self.db_key = "nu_rg"

    @property
    def cache_key(self):
        return f"detran_request_line_{self.rg}"

    def md5_hash(self, photo):
        return md5(photo.encode()).hexdigest()

    def check_request_queue(self):
        already_cached = cache.get(self.cache_key)
        if already_cached is None:
            logger.info(f"RG: {self.rg} - Busca da foto inserida na fila.")
            cache.set(self.cache_key, True)
            created = True
        else:
            logger.info(f"RG: {self.rg} - Busca da foto já foi disparada.")
            created = False

        return created

    def dispatch_request(self):
        try:
            data = request_detran_data(self.rg)
        except DetranAPIClientError as e:
            # TODO except only DetranException
            cache.delete(self.cache_key)
            raise e

        return data

    def persist_photo(self, photo):
        self.photo_dao.insert(
            row_id=self.rg,
            data={
                self.photo_column: photo,
                self.hash_column: self.md5_hash(photo),
            },
        )
        # Depois que a foto foi salva no banco, exclui registro da busca
        cache.delete(self.cache_key)

    def get_db_data(self):
        return self.data_dao.select(
            columns=["*"], parameters={self.db_key: self.rg}
        )

    def get_db_photo(self):
        return self.photo_dao.select(
            row_id=self.rg, columns=[self.photo_column]
        ).get(self.photo_column.encode(), dict())

    def wait_for_photo(self):
        sleep(self.wait_time)
        photo = self.get_db_photo()
        attempts = 1
        logger.info(f"RG: {self.rg} - Aguardando foto ser persistida no BD")
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
        joined_queue = self.check_request_queue()
        # If request just joined the queue, go search for the photo.
        # Otherwise, it was already in the queue, so wait to be persisted
        if joined_queue:
            photo = self.dispatch_request()
            self.persist_photo(photo)
        else:
            photo = self.wait_for_photo()

        return photo

    def serialize(self, result_set):
        return self.serializer_obj(result_set).data

    def get_data(self):
        logger.info(f"RG: {self.rg} - Buscando informações no BD")
        db_data = self.get_db_data()

        if not db_data:
            raise DataDoesNotExistException(
                f"Não existem dados para {self.rg}"
            )

        ser_db_data = self.serialize(db_data)

        photo = self.get_db_photo()
        if not photo:
            logger.info(
                f"RG: {self.rg} - Foto não encontrada no BD."
                "Enviando requisição para busca da foto."
            )
            photo = self.request_photo()
        else:
            logger.info(f"RG: {self.rg} - Foto encontrada no BD.")

        ser_db_data.update({"photo": photo})
        return ser_db_data

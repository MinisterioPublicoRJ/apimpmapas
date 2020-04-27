import os
import logging

from django.conf import settings
from impala.dbapi import connect as bda_connect
from impala.error import HiveServer2Error as BDA_Error
from happybase import Connection as HBaseConnection

from lupa.exceptions import QueryError



logger = logging.getLogger(__name__)
os.environ['NLS_LANG'] = 'American_America.UTF8'


def execute(query, parameters):
    with bda_connect(
        host=settings.IMPALA_HOST,
        port=settings.IMPALA_PORT
    ) as conn:
        with conn.cursor() as curs:
            try:
                curs.execute(query, parameters)
                return curs.fetchall()
            except BDA_Error as e:
                logger.error("Error on query: " + str(e))
                raise QueryError(str(e)) from e


def run_query(query, parameters=None):
    try:
        db_result = execute(query, parameters)
    except QueryError:
        return None
    if db_result and db_result[0]:
        return db_result
    return None


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

    def select(self, row_id, **kwargs):
        if isinstance(row_id, list):
            return self.get_table.rows(row_id, **kwargs)
        return self.get_table.row(row_id, **kwargs)

    def insert(self, row_id, data):
        self.get_table.put(row_id, data=data)

    def scan(self, **kwargs):
        return self.get_table.scan(**kwargs)

    def delete(self, row_id, **kwargs):
        return self.get_table.delete(row_id, **kwargs)

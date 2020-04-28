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


def get_hbase_table(table_name, server=None, timeout=None):
    hbase_server = server or settings.HBASE_SERVER
    hbase_timeout = timeout or settings.HBASE_TIMEOUT

    try:
        connection = HBaseConnection(hbase_server, timeout=hbase_timeout)
        return connection.table(table_name)
    except Exception as e:
        logger.error("Error getting table from hbase: " + str(e))
        raise Exception(str(e)) from e

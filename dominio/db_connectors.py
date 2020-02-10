import os
import logging

from decouple import config
from impala.dbapi import connect as bda_connect
from impala.error import HiveServer2Error as BDA_Error

from lupa.exceptions import QueryError


logger = logging.getLogger(__name__)
os.environ['NLS_LANG'] = 'American_America.UTF8'


def execute(query):
    with bda_connect(
        host=config('IMPALA_HOST'),
        port=config('IMPALA_PORT', cast=int)
    ) as conn:
        with conn.cursor() as curs:
            try:
                curs.execute(query)
                return curs.fetchall()
            except BDA_Error as e:
                logger.error("Error on query: " + str(e))
                raise QueryError(str(e)) from e


def run_query(query):
    try:
        db_result = execute(query)
    except QueryError:
        return None
    if db_result and db_result[0]:
        return db_result[0][0]
    return None

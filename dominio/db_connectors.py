import os
import logging

from django.conf import settings
from impala.dbapi import connect as bda_connect
from impala.error import HiveServer2Error as BDA_Error

from lupa.exceptions import QueryError
from mprj_api.exceptions import APIQueryError, APIEmptyResultError


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
        if not (db_result and db_result[0]):
            raise APIEmptyResultError()
        return db_result
    except QueryError:
        raise APIQueryError()

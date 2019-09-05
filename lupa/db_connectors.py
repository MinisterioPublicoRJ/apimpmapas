import os
import logging

from decouple import config
from psycopg2 import connect as pg_connect, Error as PG_Error
from cx_Oracle import connect as ora_connect, DatabaseError as ORA_Error
from impala.dbapi import connect as bda_connect
from impala.error import HiveServer2Error as BDA_Error

from lupa.exceptions import QueryError


logger = logging.getLogger(__name__)
os.environ['NLS_LANG'] = 'American_America.UTF8'


def execute(
    db_name,
    schema,
    table,
    columns,
    id_column,
    domain_id,
    *args,
    **kwargs
):
    conns = {
        'PG': postgres_access,
        'ORA': oracle_access,
        'BDA': bda_access,
    }

    query = generate_query(
        db_name,
        schema,
        table,
        columns,
        id_column
    )
    return conns[db_name](query, domain_id)


def generate_query(db_name, schema, table, columns, id_column):
    query = "SELECT {columns} FROM {schema}.{table} WHERE {id_column} = "\
        .format(
            columns=', '.join(columns),
            schema=schema,
            table=table,
            id_column=id_column
        )

    if db_name == 'PG':
        query += "%s"
    else:
        query += ":1"

    return query


def postgres_access(query, domain_id):
    with pg_connect(
        host=config('PG_HOST'),
        dbname=config('PG_BASE'),
        user=config('PG_USER'),
        password=config('PG_PASSWORD', "")
    ) as conn:
        with conn.cursor() as curs:
            try:
                curs.execute(query, (domain_id,))
                return curs.fetchall()
            except PG_Error as e:
                logger.error("Error on query: " + str(e))
                raise QueryError(str(e)) from e


def oracle_access(query, domain_id):
    with ora_connect(
        user=config('ORA_USER'),
        password=config('ORA_PASS'),
        dsn=config('ORA_HOST')
    ) as conn:
        with conn.cursor() as curs:
            try:
                curs.execute(query, (domain_id, ))
                return curs.fetchall()
            except ORA_Error as e:
                logger.error("Error on query: " + str(e))
                raise QueryError(str(e)) from e


def bda_access(query, domain_id):
    with bda_connect(
        host=config('IMPALA_HOST'),
        port=config('IMPALA_PORT', cast=int)
    ) as conn:
        with conn.cursor() as curs:
            try:
                curs.execute(query, (domain_id, ))
                return curs.fetchall()
            except BDA_Error as e:
                logger.error("Error on query: " + str(e))
                raise QueryError(str(e)) from e

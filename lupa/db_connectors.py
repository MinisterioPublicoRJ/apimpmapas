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

PG = 'PG'
ORA = 'ORA'
BDA = 'BDA'


def conns(db_name):
    CONNS = {
        PG: postgres_access,
        ORA: oracle_access,
        BDA: bda_access,
    }
    return CONNS[db_name]


def execute_sample(
    db_name,
    schema,
    table,
    columns,
    limit=True
):
    query = generate_query_sample(
        db_name,
        schema,
        table,
        columns,
        limit=limit
    )
    return conns(db_name)(query, [])


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
    query = generate_query(
        db_name,
        schema,
        table,
        columns,
        id_column
    )
    return conns(db_name)(query, (domain_id,))


def execute_geospatial(
    db_name,
    schema,
    table,
    geojson_column,
    id_column,
    point
):
    if db_name != PG:
        raise NotImplementedError(
            "Queries Geoespaciais são suportadas apenas por Postgres")

    query = generate_geospatial_query(
        schema,
        table,
        geojson_column,
        id_column,
        point
    )

    return conns(db_name)(query, [])


def generate_query_sample(db_name, schema, table, columns, limit=True):
    query = "SELECT {columns} FROM {schema}.{table}"\
        .format(
            columns=', '.join(columns),
            schema=schema,
            table=table
        )

    if limit:
        if db_name in ('PG', 'BDA'):
            query += ' limit 10'
        else:
            query += ' WHERE rownum < 10'
    return query


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


def generate_geospatial_query(schema, table, geojson_column,
                              id_column, point):
    point = [float(p) for p in point]
    query = """select {id_column}
               from {schema}.{table}
               where ST_Contains(
                    st_geomfromgeojson({geojson_column}),
                    st_geomfromtext('POINT({lon} {lat})')
               )""".format(
                   id_column=id_column,
                   schema=schema,
                   table=table,
                   geojson_column=geojson_column,
                   lat=point[0],
                   lon=point[1]
               )
    return query


def postgres_access(query, extra_parameters):
    with pg_connect(
        host=config('PG_HOST'),
        dbname=config('PG_BASE'),
        user=config('PG_USER'),
        password=config('PG_PASSWORD', "")
    ) as conn:
        with conn.cursor() as curs:
            try:
                curs.execute(query, extra_parameters)
                return curs.fetchall()
            except PG_Error as e:
                logger.error("Error on query: " + str(e))
                raise QueryError(str(e)) from e


def oracle_access(query, extra_parameters):
    with ora_connect(
        user=config('ORA_USER'),
        password=config('ORA_PASS'),
        dsn=config('ORA_HOST')
    ) as conn:
        with conn.cursor() as curs:
            try:
                curs.execute(query, extra_parameters)
                return curs.fetchall()
            except ORA_Error as e:
                logger.error("Error on query: " + str(e))
                raise QueryError(str(e)) from e


def bda_access(query, extra_parameters):
    with bda_connect(
        host=config('IMPALA_HOST'),
        port=config('IMPALA_PORT', cast=int)
    ) as conn:
        with conn.cursor() as curs:
            try:
                curs.execute(query, extra_parameters)
                return curs.fetchall()
            except BDA_Error as e:
                logger.error("Error on query: " + str(e))
                raise QueryError(str(e)) from e

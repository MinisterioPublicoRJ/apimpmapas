import os

from decouple import config
from psycopg2 import connect as pg_connect
from cx_Oracle import connect as ora_connect
from impala.dbapi import connect as dba_connect


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
        'DBA': dba_access,
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
        user=config('PG_USER')
    ) as conn:
        with conn.cursor() as curs:
            curs.execute(query, (domain_id,))
            return curs.fetchall()


def oracle_access(query, domain_id):
    with ora_connect(
        user=config('ORA_USER'),
        password=config('ORA_PASS'),
        dsn=config('ORA_HOST')
    ) as conn:
        with conn.cursor() as curs:
            curs.execute(query, (domain_id, ))
            return curs.fetchall()


def dba_access(query, domain_id):
    with dba_connect(
        host=config('IMPALA_HOST'),
        port=config('IMPALA_PORT', cast=int)
    ) as conn:
        with conn.cursor() as curs:
            curs.execute(query, (domain_id, ))
            return curs.fetchall()

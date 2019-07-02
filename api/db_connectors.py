from decouple import config
from psycopg2 import connect as postgres_connect


def execute(db_name, query, domain_id, *args, **kwargs):
    conns = {'PG': postgres_access}

    conns[db_name](query)

def postgres_access(query):
    with postgres_connect(
        host=config('PG_HOST'),
        dbname=config('PG_BASE'),
        user=config('PG_USER')
    ) as conn:
        with conn.cursor() as curs:
            curs.execute(query)

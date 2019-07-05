from decouple import config
from psycopg2 import connect as pg_connect


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
    conns = {'PG': postgres_access}

    query = generate_query(
        db_name,
        schema,
        table,
        columns,
        id_column
    )
    return conns[db_name](query, domain_id)


def generate_query(db_name, schema, table, columns, id_column):
    if db_name == 'PG' and schema is None:
        schema = 'public'

    query = "SELECT {columns} FROM {schema}.{table} WHERE {id_column} = %s"\
        .format(
            columns=', '.join(columns),
            schema=schema,
            table=table,
            id_column=id_column
        )

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

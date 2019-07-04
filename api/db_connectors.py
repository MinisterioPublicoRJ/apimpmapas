from decouple import config
from psycopg2 import sql as pg_sql, connect as pg_connect


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

    return conns[db_name](schema, table, columns, id_column, domain_id)


def postgres_access(schema, table, columns, id_column, domain_id):
    if schema is None:
        schema = 'public'

    query = pg_sql.SQL("SELECT {} FROM {}.{} WHERE {} = %s").format(
        pg_sql.SQL(",").join(map(pg_sql.Identifier, columns)),
        pg_sql.Identifier(schema),
        pg_sql.Identifier(table),
        pg_sql.Identifier(id_column)
    )

    with pg_connect(
        host=config('PG_HOST'),
        dbname=config('PG_BASE'),
        user=config('PG_USER')
    ) as conn:
        with conn.cursor() as curs:
            curs.execute(query, (int(domain_id), ))
            return curs.fetchall()

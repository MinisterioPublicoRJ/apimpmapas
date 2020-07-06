import datetime
import json

import cx_Oracle

from desaparecidos.queries.rank import query as q_rank


def client(db_username, db_pwd, db_host):
    orcl = cx_Oracle.connect(
        db_username,
        db_pwd,
        db_host
    )
    cursor = orcl.cursor()
    return cursor


def format_query(query, id_sinalid):
    return query.replace("{{ id_sinalid }}", id_sinalid)


def rank_query(cursor, id_sinalid):
    f_query = format_query(q_rank, id_sinalid)
    cursor.execute(f_query)
    return cursor.fetchall()


def serialize(result_set, limit=None):
    def default(o):
        if isinstance(o, (datetime.date, datetime.datetime)):
            return o.isoformat()

    columns = [
        "busca_id_sinalid",
        "candidato_id_sinalid",
        "data_nascimento",
        "score_sexo",
        "score_data_fato",
        "score_idade",
        "score_distancia",
        "score_total",
    ]
    limit = limit if limit else len(result_set)
    return json.loads(json.dumps(
        [dict(zip(columns, res)) for res in result_set[:limit]],
        default=default,
    ))


def rank(cursor, id_sinalid, limit=100):
    result_set = rank_query(cursor, id_sinalid)
    return serialize(result_set, limit) if result_set\
        else {'erro': 'ID Sinalid não encontrado'}

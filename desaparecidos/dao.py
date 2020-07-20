import datetime
import json

import cx_Oracle

from desaparecidos.queries.rank import query as q_rank


def client(db_username, db_pwd, db_host):
    orcl = cx_Oracle.connect(db_username, db_pwd, db_host, encoding="UTF-8",)
    cursor = orcl.cursor()
    return cursor


def format_query(query, id_sinalid):
    keep_DS = """
        SELECT
            SNCA1.SNCA_DK
        FROM
            SILD_DESAPARECIMENTO SDES
        INNER JOIN
            SILD_SINDICANCIA SNCA1
        ON (SNCA1.SNCA_DK = SDES.SDES_SNCA_DK AND
            SNCA1.SNCA_SISI_DK IN (1,3))
    """
    remove_DS = """
        SELECT
            SNCA2.SNCA_DK
        FROM
                SILD_INDICA_DESAPARECIMENTO SIDS
        INNER JOIN
                SILD_SINDICANCIA SNCA2
        ON (SNCA2.SNCA_DK = SIDS.SIDS_SNCA_DK AND
            SNCA2.SNCA_SISI_DK IN (1,3,4))
        INNER JOIN
                SILD_VITIMA VTMA
        ON (VTMA.VTMA_DK = SNCA2.SNCA_VTMA_DK AND
                ((VTMA.VTMA_CPF IS NULL AND VTMA.VTMA_NM_VITIMA IS NULL) OR
                (VTMA.VTMA_CPF IS NULL AND VTMA.VTMA_DT_NASCIMENTO IS NULL))
          )
    """
    table_filter = remove_DS if "DS" in id_sinalid else keep_DS
    return query.replace("{{ id_sinalid }}", id_sinalid).replace(
        "{{ filter }}", table_filter
    )


def rank_query(cursor, id_sinalid):
    f_query = format_query(q_rank, id_sinalid)
    cursor.execute(f_query)
    return cursor.fetchall()


def serialize(result_set, limit=None):
    def default(o):
        if isinstance(o, (datetime.date, datetime.datetime)):
            return o.isoformat()
        elif isinstance(o, cx_Oracle.LOB):
            return o.read()

    columns = [
        "snca_dk_cand",
        "data_fato_cand",
        "foto_cand",
        "idade_cand",
        "cor_pele_cand",
        "altura_cand",
        "bairro_cand",
        "cidade_cand",
        "uf_cand",
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
    return json.loads(
        json.dumps(
            [dict(zip(columns, res)) for res in result_set[:limit]],
            default=default,
        )
    )


# TODO: PLACE limit in the query!
def rank(cursor, id_sinalid, limit=100):
    result_set = rank_query(cursor, id_sinalid)
    return (
        serialize(result_set, limit)
        if result_set
        else {"erro": "ID Sinalid não encontrado"}
    )

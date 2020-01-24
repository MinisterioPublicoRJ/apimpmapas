import pandas

from busca_desaparecidos.dao import client, all_persons
from busca_desaparecidos.rank import calculate_scores, final_score
from django.core.cache import cache

from mprj_api.celeryconfig import app

from desaparecidos import settings as desaparecidos_settings


@app.task
def async_calculate_rank(id_sinalid, target_person):
    cursor = client(
        desaparecidos_settings.DESAPARECIDOS_DB_USER,
        desaparecidos_settings.DESAPARECIDOS_DB_PWD,
        desaparecidos_settings.DESAPARECIDOS_DB_HOST
    )
    persons = all_persons(cursor)
    score_df = calculate_scores(target_person, persons)
    final_score_df = final_score(score_df)

    data_len = desaparecidos_settings.DESAPARECIDOS_DATA_LEN
    data = final_score_df.head(data_len)
    data = data.replace({pandas.np.nan: None})

    cache_data = {
        'status': 'ready',
        'data': data.to_dict(orient='records'),
        'target_data': target_person.to_dict()
    }
    cache.set(
        id_sinalid,
        cache_data,
        timeout=desaparecidos_settings.DESAPARECIDOS_CACHE_TIMEOUT
    )

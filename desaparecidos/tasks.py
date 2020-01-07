import pandas

from busca_desaparecidos.dao import client, all_persons
from busca_desaparecidos.rank import calculate_scores, final_score
from decouple import config
from django.core.cache import cache

from mprj_api.celeryconfig import app


@app.task
def async_calculate_rank(id_sinalid, target_person):
    cursor = client(
        config('DESAPARECIDOS_DB_USER'),
        config('DESAPARECIDOS_DB_PWD'),
        config('DESAPARECIDOS_DB_HOST')
    )
    persons = all_persons(cursor)
    score_df = calculate_scores(target_person, persons)
    final_score_df = final_score(score_df)

    data_len = config('DESAPARECIDOS_DATA_LEN', cast=int)
    data = final_score_df.head(data_len)
    data = data.replace({pandas.np.nan: None})

    cache_data = {
        'status': 'ready',
        'data': data.to_dict(orient='records'),
        'target_data': target_person.to_dict()
    }
    cache.set(id_sinalid, cache_data)

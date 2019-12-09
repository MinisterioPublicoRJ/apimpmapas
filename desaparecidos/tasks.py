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

    cache_data = {'status': 'ready', 'data': final_score_df.iloc[:100]}
    cache.set(id_sinalid, cache_data)

from unittest import TestCase, mock

import pandas

from decouple import config

from desaparecidos.tasks import async_calculate_rank


class Task(TestCase):
    @mock.patch('desaparecidos.tasks.cache')
    @mock.patch('desaparecidos.tasks.final_score')
    @mock.patch('desaparecidos.tasks.calculate_scores',
                return_value='score_df')
    @mock.patch('desaparecidos.tasks.all_persons',
                return_value='persons')
    @mock.patch('desaparecidos.tasks.client')
    def test_calculate_rank(self, _client, _all_persons, _calculate_score,
                            _final_score, _cache):
        target_person = pandas.Series([1, 2, 3], index=['a', 'b', 'c'])
        final_score_df = mock.MagicMock()
        final_score_df.iloc = list(range(101))
        _final_score.return_value = final_score_df
        _client.return_value = 'cursor'
        id_sinalid = '12345'

        async_calculate_rank(id_sinalid, target_person)

        _client.assert_called_once_with(
            config('DESAPARECIDOS_DB_USER'),
            config('DESAPARECIDOS_DB_PWD'),
            config('DESAPARECIDOS_DB_HOST')
        )
        _all_persons.assert_called_once_with('cursor')
        _calculate_score.assert_called_once_with(target_person, 'persons')
        _final_score.assert_called_once_with('score_df')
        _cache.set.assert_called_once_with(
            id_sinalid,
            {'status': 'ready', 'data': list(range(100))}
        )

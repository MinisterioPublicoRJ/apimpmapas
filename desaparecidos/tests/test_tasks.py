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

        # data frame mocks
        data_mock = mock.MagicMock()
        data_replace_mock = mock.MagicMock()
        data_replace_mock.to_dict.return_value = [
            {'a': 1, 'b': 2}, {'a': 3, 'b': 4}
        ]
        data_mock.replace.return_value = data_replace_mock
        final_score_df = mock.MagicMock()
        final_score_df.head.return_value = data_mock
        _final_score.return_value = final_score_df

        # cursor mock
        _client.return_value = 'cursor'

        id_sinalid = '12345'
        async_calculate_rank(id_sinalid, target_person)

        _client.assert_called_once_with(
            config('DESAPARECIDOS_DB_USER'),
            config('DESAPARECIDOS_DB_PWD'),
            config('DESAPARECIDOS_DB_HOST')
        )
        len_data = config('DESAPARECIDOS_DATA_LEN', cast=int)

        # asserts
        _all_persons.assert_called_once_with('cursor')
        _calculate_score.assert_called_once_with(target_person, 'persons')
        _final_score.assert_called_once_with('score_df')
        final_score_df.head.assert_called_once_with(len_data)
        data_mock.replace.assert_called_once_with({pandas.np.nan: None})
        data_replace_mock.to_dict.assert_called_once_with(orient='records')
        _cache.set.assert_called_once_with(
            id_sinalid,
            {
                'status': 'ready',
                'data': [{'a': 1, 'b': 2}, {'a': 3, 'b': 4}],
                'target_data': {'a': 1, 'b': 2, 'c': 3}
            }
        )

from unittest import mock

from django.test import TestCase
from django.urls import reverse
from model_mommy.mommy import make

from lupa.cache import cache_key


class Cache(TestCase):
    def test_create_querystring_entidade(self):
        kwargs = {'entity_type': 'EST', 'domain_id': '33'}
        key_prefix = 'key_prefix'

        key = cache_key(key_prefix, kwargs)
        expected_key = 'key_prefix:EST:33'

        self.assertEqual(key, expected_key)

    def test_create_querystring_dados(self):
        kwargs = {'entity_type': 'MUN', 'domain_id': '33600', 'pk': '71'}
        key_prefix = 'key_prefix'

        key = cache_key(key_prefix, kwargs)
        expected_key = 'key_prefix:MUN:33600:71'

        self.assertEqual(key, expected_key)

    @mock.patch('lupa.views.django_cache')
    @mock.patch('lupa.serializers.execute')
    def test_insert_data_in_cache(self, _execute, _django_cache):
        expected_answer = {
            'domain_id': '33',
            'entity_type': 'Estado',
            'exibition_field': 'Rio de Janeiro',
            'geojson': None,
            'theme_list': [
                {
                    'tema': None,
                    'cor': None,
                    'data_list': [
                        {'id': 4}
                    ]
                },
                {
                    'tema': 'Segurança',
                    'cor': '#223478',
                    'data_list': [
                        {'id': 1},
                        {'id': 7}
                    ]
                },
                {
                    'tema': None,
                    'cor': None,
                    'data_list': [
                        {'id': 8},
                        {'id': 2}
                    ]
                },
                {
                    'tema': 'Saúde',
                    'cor': '#223578',
                    'data_list': [
                        {'id': 5}
                    ]
                }
            ]
        }

        _execute.return_value = [('Rio de Janeiro', 'mock_geo')]

        estado = make('lupa.Entidade', name='Estado', abreviation='EST')
        municipio = make('lupa.Entidade', abreviation='MUN')

        seguranca = make('lupa.TemaDado', name='Segurança', color='#223478')
        saude = make('lupa.TemaDado', name='Saúde', color='#223578')

        make('lupa.Dado', id=1, entity_type=estado, theme=seguranca, order=2)
        make('lupa.Dado', id=2, entity_type=estado, theme=None, order=5)
        make('lupa.Dado', id=3, entity_type=municipio, order=7)
        make('lupa.Dado', id=4, entity_type=estado, theme=None, order=1)
        make('lupa.Dado', id=5, entity_type=estado, theme=saude, order=8)
        make('lupa.Dado', id=6, entity_type=municipio, order=6)
        make('lupa.Dado', id=7, entity_type=estado, theme=seguranca, order=3)
        make('lupa.Dado', id=8, entity_type=estado, theme=None, order=4)

        url = reverse('lupa:detail_entidade', args=('EST', '33',))

        resp = self.client.get(url)
        resp_json = resp.json()

        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp_json, expected_answer)
        _django_cache.set.assert_called_once_with(
            'lupa_entidade:EST:33',
            expected_answer
        )

from unittest import TestCase, mock

from lupa.cache import cache_key


class Cache(TestCase):
    def test_create_querystring_hash(self):
        token = 1234
        args_list = ['key 1']
        kwargs = {'key 1': 'MUN', 'key 2': 56789}

        key = cache_key(args_list, kwargs, token)
        expected_key = '50491abb929620e598b27d56d101eef2_'\
            '81dc9bdb52d04dc20036dbd8313ed055'

        self.assertEqual(key, expected_key)

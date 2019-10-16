from unittest import TestCase

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

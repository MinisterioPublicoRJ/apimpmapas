from unittest import TestCase

from desaparecidos.utils import paginate


class TestUtils(TestCase):
    def test_paginate_data(self):
        data = {'key 1': list(range(20)), 'key 2': list(range(20, 40))}

        page_data = paginate(data, page=1, page_size=10)

        expected_data = {
            'key 1': list(range(10)),
            'key 2': list(range(20, 30))
        }
        self.assertEqual(page_data, expected_data)

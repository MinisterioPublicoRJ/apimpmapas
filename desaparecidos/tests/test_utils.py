from unittest import TestCase

from desaparecidos.utils import paginate, previous_next_page


class TestUtils(TestCase):
    def test_paginate_data(self):
        data = [
            {'key 1': x, 'key 2': y} for x, y in zip(range(20), range(20, 40))
        ]

        page_data = paginate(data, page=1, page_size=10)

        expected_data = [
            {'key 1': x, 'key 2': y} for x, y in zip(range(10), range(20, 30))
        ]
        self.assertEqual(page_data, expected_data)

    def test_paginate_data_2(self):
        data = [
            {'key 1': x, 'key 2': y}
            for x, y in zip(range(100), range(100, 200))
        ]

        page_data = paginate(data, page=2, page_size=10)

        expected_data = [
            {'key 1': x, 'key 2': y}
            for x, y in zip(range(10, 20), range(110, 120))
        ]
        self.assertEqual(page_data, expected_data)

    def test_paginate_data_page_size(self):
        data = [
            {'key 1': x, 'key 2': y}
            for x, y in zip(range(100), range(100, 200))
        ]

        page_data = paginate(data, page=3, page_size=20)

        expected_data = [
            {'key 1': x, 'key 2': y}
            for x, y in zip(range(40, 60), range(140, 160))
        ]
        self.assertEqual(page_data, expected_data)

    def test_next_page_url(self):
        base_url = 'http://base.com'
        page = 1
        data_len = 100
        page_size = 10

        page_url = previous_next_page(
            base_url,
            page,
            data_len,
            page_size
        )
        expected = {
            'self': 'http://base.com?page=1',
            'first': 'http://base.com?page=1',
            'prev': None,
            'next': 'http://base.com?page=2',
            'last': 'http://base.com?page=10'
        }

        self.assertEqual(page_url, expected)

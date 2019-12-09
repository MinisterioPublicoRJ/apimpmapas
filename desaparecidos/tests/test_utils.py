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

    def test_paginate_data_2(self):
        data = {'key 1': list(range(100)), 'key 2': list(range(100, 200))}

        page_data = paginate(data, page=2, page_size=10)

        expected_data = {
            'key 1': list(range(10, 20)),
            'key 2': list(range(110, 120))
        }
        self.assertEqual(page_data, expected_data)

    def test_paginate_data_page_size(self):
        data = {'key 1': list(range(100)), 'key 2': list(range(100, 200))}

        page_data = paginate(data, page=3, page_size=20)

        expected_data = {
            'key 1': list(range(40, 60)),
            'key 2': list(range(140, 160))
        }
        self.assertEqual(page_data, expected_data)

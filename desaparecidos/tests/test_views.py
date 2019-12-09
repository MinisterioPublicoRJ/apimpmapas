from django.shortcuts import reverse
from django.test import TestCase


class TestDesaparecidos(TestCase):
    def test_search_id_sinalid(self):
        url = reverse(
            'desaparecidos:busca',
            kwargs={'id_sinalid': '12345'}
        )

        resp = self.client.post(url)

        self.assertEqual(resp.status_code, 200)

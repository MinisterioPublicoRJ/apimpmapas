from django.test import TestCase
from django.urls import reverse


class TestSuaPromotoria(TestCase):
    def test_correct_response(self):
        url = reverse('dominio:radar-suapromotoria', args=('1', ))

        resp = self.client.get(url)

        self.assertEqual(resp.status_code, 200)

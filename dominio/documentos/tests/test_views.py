from django.test import TestCase
from django.urls import reverse


class TestDownloadMinutaPrescricao(TestCase):
    def test_correct_response(self):
        docu_dk = '12345'
        url = reverse('dominio:minuta-prescricao', args=(docu_dk,))
        resp = self.client.get(url)

        self.assertEqual(resp.status_code, 200)

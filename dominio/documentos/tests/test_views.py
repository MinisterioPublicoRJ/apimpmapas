from unittest import mock

from django.http import HttpResponse
from django.test import TestCase
from django.urls import reverse

from dominio.documentos.controllers import MinutaPrescricaoController


class TestDownloadMinutaPrescricao(TestCase):
    @mock.patch.object(MinutaPrescricaoController, "render")
    def test_correct_response(self, _render):
        mock_resp = HttpResponse(status=200)
        _render.return_value = mock_resp

        docu_dk = '12345'
        url = reverse('dominio:minuta-prescricao', args=(docu_dk,))
        resp = self.client.get(url)

        self.assertEqual(resp.status_code, 200)

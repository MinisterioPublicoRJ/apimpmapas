from django.test import TestCase
from django.urls import reverse


class TestDetranProxyView(TestCase):
    def test_correct_response(self):
        url = reverse("proxies:foto-detran", kwargs={"rg": "12345"})

        resp = self.client.get(url)

        assert resp.status_code == 200

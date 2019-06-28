from django.test import TestCase
from django.urls import reverse

from model_mommy.mommy import make


class EntidadeViewTest(TestCase):

    def test_get_entidade(self):
        entidade_obj = make(
            'api.Entidade',
            entity_type='MUN',
            domain_id=1
        )

        url = reverse('api:detail_entidade', args=('MUN', '1',))

        resp = self.client.get(url)
        resp_json = resp.json()

        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp_json['title'], entidade_obj.title)

    def test_get_entidade_404(self):
        make('api.Entidade', entity_type='MUN', domain_id=404)

        url = reverse('api:detail_entidade', args=('MUN', '1',))

        resp = self.client.get(url)

        self.assertEqual(resp.status_code, 404)

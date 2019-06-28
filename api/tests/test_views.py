from django.test import TestCase
from django.urls import reverse

from model_mommy.mommy import make


class EntidadeViewTest(TestCase):

    def test_get_entidade(self):
        entidade_obj = make('api.Entidade', entity_type__name='municipio', domain_id=1)

        url = reverse('api:detail_entidade', args=('municipio', '1',))

        resp = self.client.get(url)
        resp_json = resp.json()

        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp_json['title'], entidade_obj.title)
        

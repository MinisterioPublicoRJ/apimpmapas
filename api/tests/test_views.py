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


class ListDadosViewTest(TestCase):
    def test_get_lista_dados(self):
        """Deve retornar dados referentes ao tipo de entidade chamado"""
        make('api.Entidade', entity_type='MUN', domain_id=1)
        make('api.Dado', entity_type='EST', _quantity=2)
        dado_object_mun = make('api.Dado', entity_type='MUN', _quantity=2)

        url = reverse('api:detail_entidade', args=('MUN', '1',))

        resp = self.client.get(url)
        resp_json = resp.json()

        self.assertEqual(resp.status_code, 200)
        self.assertEqual(
            len(resp_json['data_list']),
            2
        )
        self.assertEqual(
            resp_json['data_list'][0]['id'],
            dado_object_mun[0].id
        )
        self.assertEqual(
            resp_json['data_list'][1]['id'],
            dado_object_mun[1].id
        )

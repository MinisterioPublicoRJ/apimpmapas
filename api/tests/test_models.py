from unittest import TestCase

import pytest
from model_mommy.mommy import make


@pytest.mark.django_db(transaction=True)
class TestStringRepresentation(TestCase):

    def test_string_entidade(self):
        obj = make('api.Entidade', title='teste_nome')

        self.assertEqual(obj.__str__(), 'teste_nome')

    def test_string_dado(self):
        obj = make('api.Dado', title='teste_nome')

        self.assertEqual(obj.__str__(), 'teste_nome')

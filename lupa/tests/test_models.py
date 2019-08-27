from unittest import TestCase

import pytest
from model_mommy.mommy import make


@pytest.mark.django_db(transaction=True)
class TestStringRepresentation(TestCase):

    def test_string_entidade(self):
        obj = make('lupa.Entidade', name='teste_nome')

        self.assertEqual(obj.__str__(), 'teste_nome')

    def test_string_dado(self):
        obj = make('lupa.Dado', title='teste_nome')

        self.assertEqual(obj.__str__(), 'teste_nome')

    def test_string_icone(self):
        obj = make('lupa.Icone', name='teste_nome')

        self.assertEqual(obj.__str__(), 'teste_nome')

    def test_string_tipo_dado(self):
        obj = make('lupa.TipoDado', name='teste_nome')

        self.assertEqual(obj.__str__(), 'teste_nome')

    def test_string_tema_dado(self):
        obj = make('lupa.TemaDado', name='teste_nome')

        self.assertEqual(obj.__str__(), 'teste_nome')

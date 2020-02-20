from unittest import TestCase

import pytest
from model_bakery.baker import make


@pytest.mark.django_db(transaction=True)
class TestStringRepresentation(TestCase):

    def test_string_area(self):
        obj = make('mprj_plus.Area', nome='teste_nome')

        self.assertEqual(obj.__str__(), 'teste_nome')

    def test_string_tema(self):
        obj = make('mprj_plus.Tema', titulo='teste_nome')

        self.assertEqual(obj.__str__(), 'teste_nome')

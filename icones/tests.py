from django.test import TestCase
from model_mommy.mommy import make
import pytest


# Create your tests here.
@pytest.mark.django_db(transaction=True)
class TestStringRepresentation(TestCase):

    def test_string_icone(self):
        obj = make('icones.Icone', name='teste_nome')

        self.assertEqual(obj.__str__(), 'teste_nome')

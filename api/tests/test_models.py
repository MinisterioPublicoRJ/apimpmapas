from unittest import TestCase

import pytest

from api.models import (
    TipoEntidade,
    TipoDado,
    Entidade
)


@pytest.mark.django_db(transaction=True)
class TestStringRepresentation(TestCase):

    def test_string_tipo_entidade(self):
        model = TipoEntidade()
        model.name = 'teste_nome'
        model.save()

        self.assertEqual(model.__str__(), 'teste_nome')

    def test_string_tipo_dado(self):
        model = TipoDado()
        model.name = 'teste_nome'
        model.save()

        self.assertEqual(model.__str__(), 'teste_nome')

    def test_string_entidade(self):
        entity_type = TipoEntidade()
        entity_type.name = 'teste_entidade'
        entity_type.save()

        model = Entidade()
        model.title = 'teste_nome'
        model.entity_type = entity_type
        model.save()

        self.assertEqual(model.__str__(), 'teste_entidade - teste_nome')

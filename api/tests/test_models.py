from unittest import TestCase

import pytest

from api.models import (
    TipoEntidadeModel,
    TipoDadoModel,
    EntidadeModel
)


@pytest.mark.django_db(transaction=True)
class TestStringRepresentation(TestCase):

    def test_string_tipo_entidade_model(self):
        model = TipoEntidadeModel()
        model.name = 'teste_nome'
        model.save()

        self.assertEqual(model.__str__(), 'teste_nome')

    def test_string_tipo_dado_model(self):
        model = TipoDadoModel()
        model.name = 'teste_nome'
        model.save()

        self.assertEqual(model.__str__(), 'teste_nome')

    def test_string_entidade_model(self):
        entity_type = TipoEntidadeModel()
        entity_type.name = 'teste_entidade'
        entity_type.save()

        model = EntidadeModel()
        model.title = 'teste_nome'
        model.entity_type = entity_type
        model.save()

        self.assertEqual(model.__str__(), 'teste_entidade - teste_nome')

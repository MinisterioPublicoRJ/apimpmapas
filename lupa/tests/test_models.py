from unittest import TestCase

import pytest
from django.core.exceptions import ValidationError
from model_mommy.mommy import make
from lupa.models import (
    MANDATORY_OSM_PARAMETERS,
    MANDATORY_GEOJSON_COLUMN,
    SUBURB,
    ORACLE,
    POSTGRES,
    ONLY_POSTGIS_SUPORTED
)


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

    def test_string_grupo(self):
        obj = make('lupa.Grupo', name='teste_nome')

        self.assertEqual(obj.__str__(), 'teste_nome')


@pytest.mark.django_db(transaction=True)
class TestEntityModel(TestCase):

    def test_validate_mandatory_osm_map_all_empty(self):
        entity = make('lupa.Entidade', name="Primeiro")
        entity.geojson_column = ''
        entity.osm_value_attached = None
        entity.osm_default_level = False
        entity.clean()

    def test_validate_mandatory_osm_map_value_attached_without_geojson(self):
        entity = make('lupa.Entidade', name="Primeiro")
        entity.geojson_column = ''
        entity.osm_value_attached = "yay"
        entity.osm_default_level = False

        with self.assertRaises(ValidationError) as cm:
            entity.clean()

        exception = cm.exception.message_dict
        self.assertIn('geojson_column', exception)
        self.assertEqual(len(exception.keys()), 1)
        self.assertEqual(
            exception['geojson_column'][0],
            MANDATORY_OSM_PARAMETERS
        )

    def test_validate_mandatory_osm_map_osm_default_without_geojson(self):
        entity = make('lupa.Entidade', name="Primeiro")
        entity.geojson_column = ''
        entity.osm_value_attached = None
        entity.osm_default_level = True

        with self.assertRaises(ValidationError) as cm:
            entity.clean()

        exception = cm.exception.message_dict
        self.assertIn('geojson_column', exception)
        self.assertEqual(len(exception.keys()), 1)
        self.assertEqual(
            exception['geojson_column'][0],
            MANDATORY_OSM_PARAMETERS
        )

    def test_validate_mandatory_osm_map_without_geojson_with_both_detais(self):
        entity = make('lupa.Entidade', name="Primeiro")
        entity.geojson_column = ''
        entity.osm_value_attached = "yay"
        entity.osm_default_level = True

        with self.assertRaises(ValidationError) as cm:
            entity.clean()

        exception = cm.exception.message_dict
        self.assertIn('geojson_column', exception)
        self.assertEqual(len(exception.keys()), 1)
        self.assertEqual(
            exception['geojson_column'][0],
            MANDATORY_OSM_PARAMETERS
        )

    def test_validate_mandatory_osm_map_with_geojson_without_both_detais(self):
        entity = make('lupa.Entidade', name="Primeiro")
        entity.geojson_column = 'column'
        entity.osm_value_attached = ""
        entity.osm_default_level = False

        with self.assertRaises(ValidationError) as cm:
            entity.clean()

        exception = cm.exception.message_dict
        self.assertIn('geojson_column', exception)
        self.assertEqual(len(exception.keys()), 1)
        self.assertEqual(
            exception['geojson_column'][0],
            MANDATORY_GEOJSON_COLUMN
        )

    def test_validate_mandatory_osm_map_with_geojson_with_value_attached(self):
        entity = make('lupa.Entidade', name="Primeiro")
        entity.geojson_column = 'column'
        entity.osm_value_attached = "attached"
        entity.osm_default_level = False
        entity.clean()

    def test_validate_mandatory_osm_map_with_geojson_with_default_level(self):
        entity = make('lupa.Entidade', name="Primeiro")
        entity.geojson_column = 'column'
        entity.osm_value_attached = ""
        entity.osm_default_level = True
        entity.clean()

    def test_validate_multiple_osm_map_value_attached(self):
        entity = make('lupa.Entidade', name="Primeiro")
        entity.geojson_column = 'column'
        entity.osm_value_attached = SUBURB
        entity.osm_default_level = False
        entity.clean()
        entity.save()

        entity = make('lupa.Entidade', name="Segundo")
        entity.geojson_column = 'column'
        entity.osm_value_attached = SUBURB
        entity.osm_default_level = False

        with self.assertRaises(ValidationError) as cm:
            entity.clean()

        exception = cm.exception.message_dict
        self.assertIn('osm_value_attached', exception)
        self.assertEqual(len(exception.keys()), 1)
        self.assertEqual(
            exception['osm_value_attached'][0],
            'A Entidade Primeiro já possui a propriedade Bairro'
        )

    def test_validate_multiple_osm_map_default_level(self):
        entity = make('lupa.Entidade', name="Primeiro")
        entity.geojson_column = 'column'
        entity.osm_value_attached = None
        entity.osm_default_level = True
        entity.clean()
        entity.save()

        entity = make('lupa.Entidade', name="Segundo")
        entity.geojson_column = 'column'
        entity.osm_value_attached = None
        entity.osm_default_level = True

        with self.assertRaises(ValidationError) as cm:
            entity.clean()

        exception = cm.exception.message_dict
        self.assertIn('osm_default_level', exception)
        self.assertEqual(len(exception.keys()), 1)
        self.assertEqual(
            exception['osm_default_level'][0],
            ('A Entidade Primeiro já responde pela '
             'busca padrão de geolocalização')
        )

    def test_validate_mandatory_osm_map_with_different_database(self):
        entity = make('lupa.Entidade', name="Primeiro")
        entity.geojson_column = 'column'
        entity.osm_value_attached = SUBURB
        entity.database = ORACLE

        with self.assertRaises(ValidationError) as cm:
            entity.clean()

        exception = cm.exception.message_dict
        self.assertIn('geojson_column', exception)
        self.assertEqual(len(exception.keys()), 1)
        self.assertEqual(
            exception['geojson_column'][0],
            ONLY_POSTGIS_SUPORTED
        )

    def test_validate_mandatory_osm_map_with_correct_database(self):
        entity = make('lupa.Entidade', name="Primeiro")
        entity.geojson_column = 'column'
        entity.osm_value_attached = SUBURB
        entity.database = POSTGRES
        entity.clean()

from datetime import datetime as dt
from unittest import TestCase

from freezegun import freeze_time

import pytest
from django.core.exceptions import ValidationError
from django.db.models.query import QuerySet
from model_mommy.mommy import make
from lupa.models import (
    MANDATORY_OSM_PARAMETERS,
    MANDATORY_GEOJSON_COLUMN,
    SUBURB,
    ORACLE,
    POSTGRES,
    ONLY_POSTGIS_SUPORTED,
    Entidade,
    DadoEntidade,
    DadoDetalhe,
    CacheManager
)


@pytest.mark.django_db(transaction=True)
class TestStringRepresentation(TestCase):

    def test_string_entidade(self):
        obj = make('lupa.Entidade', name='teste_nome')

        self.assertEqual(obj.__str__(), 'teste_nome')

    def test_string_dado(self):
        obj = make('lupa.DadoEntidade', title='teste_nome')

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

    def test_self_exclude(self):
        entity = make('lupa.Entidade', name='Primeiro')
        entity.geojson_column = 'column'
        entity.osm_value_attached = SUBURB
        entity.database = POSTGRES

        self.assertEqual(entity.clean(), None)

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


@pytest.mark.django_db(transaction=True)
class ConvertCacheTimeout(TestCase):
    def test_convert_entity_cache_timeout_to_seconds(self):
        entity = make('lupa.Entidade', cache_timeout=7)
        seconds = 604800

        self.assertEqual(entity.cache_timeout, seconds)

    def test_convert_data_entidade_cache_timeout_to_seconds(self):
        entity = make('lupa.DadoEntidade', cache_timeout=10)
        seconds = 864000

        self.assertEqual(entity.cache_timeout, seconds)

    def test_convert_data_detalhe_cache_timeout_to_seconds(self):
        entity = make('lupa.DadoDetalhe', cache_timeout=10)
        seconds = 864000

        self.assertEqual(entity.cache_timeout, seconds)


@pytest.mark.django_db(transaction=True)
class RetrieveExpiringCacheObjects(TestCase):
    def test_convert_seconds_to_days(self):
        seconds = 604800
        manager = CacheManager()
        days = manager.to_days(seconds)
        expected_days = 7

        self.assertEqual(days, expected_days)

    @freeze_time('2019-10-22 12:00:00')
    def test_retrieve_expiring_cache_data_entidade(self):
        expired_data_obj = make(
            'lupa.DadoEntidade',
            cache_timeout=7,
            last_cache_update=dt(2019, 10, 15, 12, 0, 0)
        )
        make(
            'lupa.DadoEntidade',
            cache_timeout=7,
            last_cache_update=dt(2019, 10, 20, 12, 0, 0)
        )

        expiring_data = DadoEntidade.cache.expiring()

        self.assertEqual(len(expiring_data), 1)
        self.assertIsInstance(expiring_data, QuerySet)
        self.assertEqual(expiring_data[0], expired_data_obj)

    @freeze_time('2019-10-22 12:00:00')
    def test_retrieve_expiring_cache_data_detalhe(self):
        expired_data_obj = make(
            'lupa.DadoDetalhe',
            cache_timeout=7,
            last_cache_update=dt(2019, 10, 15, 12, 0, 0)
        )
        make(
            'lupa.DadoDetalhe',
            cache_timeout=7,
            last_cache_update=dt(2019, 10, 20, 12, 0, 0)
        )

        expiring_data = DadoDetalhe.cache.expiring()

        self.assertEqual(len(expiring_data), 1)
        self.assertIsInstance(expiring_data, QuerySet)
        self.assertEqual(expiring_data[0], expired_data_obj)

    @freeze_time('2019-10-22 12:00:00')
    def test_retrieve_expiring_cache_entity(self):
        expired_entity_obj = make(
            'lupa.Entidade',
            cache_timeout=7,
            last_cache_update=dt(2019, 10, 15, 12, 0, 0)
        )
        # This one is also expired. Ignore hours, just consider days
        make(
            'lupa.Entidade',
            cache_timeout=7,
            last_cache_update=dt(2019, 10, 15, 14, 0, 0)
        )

        expiring_entity = Entidade.cache.expiring()

        self.assertEqual(len(expiring_entity), 2)
        self.assertIsInstance(expiring_entity, QuerySet)
        self.assertEqual(expiring_entity[0], expired_entity_obj)

    def test_retrieve_expiring_object_with_null_last_update(self):
        make(
            'lupa.Entidade',
            cache_timeout=7,
            last_cache_update=None
        )

        expiring_entity = Entidade.cache.expiring()

        self.assertEqual(expiring_entity.count(), 1)

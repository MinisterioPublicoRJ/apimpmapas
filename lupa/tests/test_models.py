from datetime import datetime as dt
from unittest import TestCase, mock

from freezegun import freeze_time

import pytest
from django.core.exceptions import ValidationError
from django.db.models.query import QuerySet
from model_mommy.mommy import make

from lupa.cache import ENTITY_KEY_PREFIX
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
class RetrieveExpiringCacheObjects(TestCase):
    @freeze_time('2019-10-22 12:00:00')
    def test_retrieve_expiring_cache_data_entidade(self):
        expired_data_obj = make(
            'lupa.DadoEntidade',
            cache_timeout_days=7,
            last_cache_update=dt(2019, 10, 15, 12, 0, 0)
        )
        make(
            'lupa.DadoEntidade',
            cache_timeout_days=7,
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
            cache_timeout_days=7,
            last_cache_update=dt(2019, 10, 15, 12, 0, 0)
        )
        make(
            'lupa.DadoDetalhe',
            cache_timeout_days=7,
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
            cache_timeout_days=7,
            last_cache_update=dt(2019, 10, 15, 12, 0, 0)
        )
        # This one is also expired. Ignore hours, just consider days
        make(
            'lupa.Entidade',
            cache_timeout_days=7,
            last_cache_update=dt(2019, 10, 15, 14, 0, 0)
        )

        expiring_entity = Entidade.cache.expiring()

        self.assertEqual(len(expiring_entity), 2)
        self.assertIsInstance(expiring_entity, QuerySet)
        self.assertEqual(expiring_entity[0], expired_entity_obj)

    def test_retrieve_expiring_object_with_null_last_update(self):
        make(
            'lupa.Entidade',
            cache_timeout_days=7,
            last_cache_update=None
        )

        expiring_entity = Entidade.cache.expiring()

        self.assertEqual(expiring_entity.count(), 1)


@pytest.mark.django_db(transaction=True)
class TestDataModel(TestCase):
    def setUp(self):
        self.dadoBase = make('lupa.DadoEntidade')
        self.dadoDetalhar = make('lupa.DadoEntidade', show_box=True)
        self.colunaDetalhar1 = make('lupa.ColunaDado', dado=self.dadoDetalhar)
        self.colunaDetalhar2 = make('lupa.ColunaDado', dado=self.dadoDetalhar)

    def test_main_work(self):
        self.dadoDetalhar.copy_to_detail(self.dadoBase)
        self.assertFalse(self.dadoDetalhar.show_box)

        detalhes = self.dadoBase.data_details.all()
        self.assertEqual(len(detalhes), 1)

        detalhar = {
            'title': self.dadoDetalhar.title,
            'exibition_field': self.dadoDetalhar.exibition_field,
            'database': self.dadoDetalhar.database,
            'schema': self.dadoDetalhar.schema,
            'table': self.dadoDetalhar.table,
            'limit_fetch': self.dadoDetalhar.limit_fetch,
            'data_type': self.dadoDetalhar.data_type
        }

        detalhe = detalhes.first()
        detalhado = {
            'title': detalhe.title,
            'exibition_field': detalhe.exibition_field,
            'database': detalhe.database,
            'schema': detalhe.schema,
            'table': detalhe.table,
            'limit_fetch': detalhe.limit_fetch,
            'data_type': detalhe.data_type
        }

        self.assertEqual(detalhe.dado_main, self.dadoBase)
        self.assertEqual(detalhar, detalhado)

        colunas_detalhar = []
        for coluna in self.dadoDetalhar.column_list.all():
            colunas_detalhar.append({
                'name': coluna.name,
                'info_type': coluna.info_type
            })
        colunas_detalhado = []
        for coluna in self.dadoDetalhar.column_list.all():
            colunas_detalhado.append({
                'name': coluna.name,
                'info_type': coluna.info_type
            })
        self.assertCountEqual(colunas_detalhar, colunas_detalhado)


@pytest.mark.django_db(transaction=True)
class RenewCacheWhenIsCachebleIsChanged(TestCase):
    @mock.patch('lupa.models.asynch_remove_from_cache')
    def test_asynch_remove_entity_from_cache(self, _asynch_remove):
        """The the model field is_cacheable is set to False
        start a async task to remove the given entity from cache"""
        entidade = make('lupa.Entidade', is_cacheable=True)
        entidade.is_cacheable = False
        entidade.save()

        expected_queryset = Entidade.objects.filter(pk=entidade.pk)
        asynch_call = _asynch_remove.delay.call_args_list[0][0]

        self.assertEqual(asynch_call[0], ENTITY_KEY_PREFIX)
        self.assertEqual(asynch_call[1], ['abreviation'])
        self.assertEqual(asynch_call[2].first(), expected_queryset.first())

    @mock.patch('lupa.models.asynch_repopulate_cache_entity')
    def test_asynch_repopulate_entity_from_cache(self, _asynch_repopulate):
        entidade = make('lupa.Entidade', is_cacheable=False)
        entidade.is_cacheable = True
        entidade.save()

        expected_queryset = Entidade.objects.filter(pk=entidade.pk)
        asynch_call = _asynch_repopulate.delay.call_args_list[0][0]

        self.assertEqual(asynch_call[0], ENTITY_KEY_PREFIX)
        self.assertEqual(asynch_call[1].first(), expected_queryset.first())

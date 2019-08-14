import json
from unittest import mock

from django.test import TestCase

from lupa.serializers import EntidadeSerializer, QueryError

from model_mommy.mommy import make


class MapTest(TestCase):

    @mock.patch('lupa.serializers.execute')
    def test_map_json(self, _execute):
        entidade = make(
            'lupa.Entidade',
            abreviation='ORG'
        )
        make('lupa.Mapa', entity=entidade)

        coord = {
            "type": "Point",
            "coordinates": [
                -43.1698636,
                -22.9075676
            ]
        }

        features = [{
            "type": "Feature",
            "properties": {
                'name': 'Name',
                'entity_link_type': 'CRA',
                'entity_link_id': '2'
            },
            "geometry": coord
        }]

        _execute.side_effect = [
            [('mock_name', )],
            [(json.dumps(coord), 'Name', 'CRA', '2')],
        ]

        ent_ser = EntidadeSerializer(entidade, domain_id='99').data
        self.assertEqual(ent_ser['geojson'], features)

    @mock.patch('lupa.serializers.execute')
    def test_map_error(self, _execute):
        _execute.side_effect = QueryError('test error')

        entidade = make(
            'lupa.Entidade',
            abreviation='ORG'
        )
        make('lupa.Mapa', entity=entidade)

        ent_ser = EntidadeSerializer(entidade, domain_id='99').data
        self.assertEqual(ent_ser['geojson'], None)

import json
from unittest import mock

from django.test import TestCase

from api.serializers import EntidadeSerializer

from model_mommy.mommy import make


class MapTest(TestCase):

    @mock.patch('api.serializers.execute')
    def test_map_json(self, _execute):
        entidade = make(
            'api.Entidade',
            entity_type='ORG',
            map_table='tabela',
            map_column_id='id',
            map_column_geom='geom'
        )

        coord = {
            "type": "Point",
            "coordinates": [
                -43.1698636,
                -22.9075676
            ]
        }

        _execute.return_value = [[json.dumps(coord), ], ]

        ent_ser = EntidadeSerializer(entidade, entity_type='ORG').data

        self.assertEqual(ent_ser['geojson'], coord)

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
            abreviation='ORG',
            geom_column='geom'
        )

        coord = {
            "type": "Point",
            "coordinates": [
                -43.1698636,
                -22.9075676
            ]
        }

        _execute.return_value = [['Sbrubbles', json.dumps(coord), ], ]

        ent_ser = EntidadeSerializer(entidade, domain_id='99').data

        self.assertEqual(ent_ser['geojson'], coord)

    # TODO: Teste para caso de erro

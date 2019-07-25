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
            geom_column_mapa='geom'
        )

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
        # import ipdb; ipdb.set_trace()

        ent_ser = EntidadeSerializer(entidade, domain_id='99').data
        self.assertEqual(ent_ser['geojson'], features)

    # TODO: Teste para caso de erro

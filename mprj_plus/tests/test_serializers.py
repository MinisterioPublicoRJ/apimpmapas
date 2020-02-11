from datetime import datetime

from django.test import TestCase
from model_bakery.baker import make

from mprj_plus.serializers import AreaSerializer, TemaSerializer


class AreaSerializeTest(TestCase):

    def test_area_count(self):
        area_1 = make('mprj_plus.Area', created_at=datetime.now())
        area_2 = make('mprj_plus.Area', created_at=datetime.now())
        area_3 = make('mprj_plus.Area', created_at=datetime.now())
        make(
            'mprj_plus.Tema',
            area_mae=area_1,
            created_at=datetime.now()
        )
        make(
            'mprj_plus.Tema',
            area_mae=area_2,
            created_at=datetime.now()
        )
        make(
            'mprj_plus.Tema',
            area_mae=area_3,
            areas_correlatas=[area_1, ],
            created_at=datetime.now()
        )
        make(
            'mprj_plus.Tema',
            area_mae=area_3,
            areas_correlatas=[area_1, area_2],
            created_at=datetime.now()
        )
        area_1_ser = AreaSerializer(area_1).data
        area_2_ser = AreaSerializer(area_2).data
        area_3_ser = AreaSerializer(area_3).data

        self.assertEqual(area_1_ser['count'], 3)
        self.assertEqual(area_2_ser['count'], 2)
        self.assertEqual(area_3_ser['count'], 2)


class TemaSerializeTest(TestCase):

    def test_tema_endpoint(self):
        titulo = 'titulo tema'
        expected = 'titulotema'
        tema = make('mprj_plus.Tema', titulo=titulo, created_at=datetime.now())

        tema_ser = TemaSerializer(tema).data

        self.assertEqual(tema_ser['endpoint'], expected)

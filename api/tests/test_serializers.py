from unittest import TestCase, mock

import pytest

from model_mommy.mommy import make

from api.serializers import DadoSerializer


@pytest.mark.django_db(transaction=True)
class DadoSerializerTest(TestCase):

    @mock.patch('api.serializers.execute')
    def test_data_type_serializing(self, _execute):
        dado_tg = make('api.Dado', data_type='TEX_GDE')
        dado_tp = make('api.Dado', data_type='TEX_PEQ')
        dado_tpd = make('api.Dado', data_type='TEX_PEQ_DEST')
        dado = make('api.Dado', data_type='NAO_DETERMINADO')

        dado_tg_ser = DadoSerializer(dado_tg, domain_id='00').data
        dado_tp_ser = DadoSerializer(dado_tp, domain_id='00').data
        dado_tpd_ser = DadoSerializer(dado_tpd, domain_id='00').data
        dado_ser = DadoSerializer(dado, domain_id='00').data

        self.assertEqual(dado_tg_ser['data_type'], 'texto_grande')
        self.assertEqual(dado_tp_ser['data_type'], 'texto_pequeno')
        self.assertEqual(dado_tpd_ser['data_type'], 'texto_pequeno_destaque')
        self.assertEqual(dado_ser['data_type'], 'tipo_desconhecido')

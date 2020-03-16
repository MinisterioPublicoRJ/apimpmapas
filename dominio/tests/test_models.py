from unittest import mock, TestCase

from django.conf import settings

from dominio.models import Alerta


class TestAlertaModels(TestCase):
    @mock.patch("dominio.models.run_query")
    def test_validos_por_orgaos(self, _run_query):
        orgao_id = 12345
        _run_query.return_value = [
            (
                'data 1',
                'data 2',
                0,
                'data 3',
                'data 4',
                'data 5',
                'data 6',
                'data 7',
                int(orgao_id),
                'data 8',
                -1,
            )
        ]
        resp = Alerta.validos_por_orgao(orgao_id)
        expected_resp = [
            {
                'doc_dk': 'data 1',
                'num_doc': 'data 2',
                'num_ext': 0,
                'etiqueta': 'data 3',
                'classe_doc': 'data 4',
                'data_alerta': 'data 5',
                'orgao': 'data 6',
                'classe_hier': 'data 7',
                'dias_passados': 12345,
                'descricao': 'data 8',
                'sigla': -1}
        ]

        _run_query.assert_called_once_with(
            Alerta.query.format(schema=settings.TABLE_NAMESPACE),
            {"orgao_id": orgao_id},
        )
        self.assertEqual(resp, expected_resp)

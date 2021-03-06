from unittest import mock

from django.test import TestCase

from dominio.pip.utils import (
    get_orgaos_same_aisps,
    get_top_n_by_aisp,
    get_aisps,
)


class UtilsPIPTest(TestCase):
    @mock.patch("dominio.pip.utils.run_query")
    def test_get_orgaos_same_aisps(self, _run_query):
        _run_query.return_value = [
            (1, 1, "AISP1", 200),
            (1, 2, "AISP2", 200),
            (2, 1, "AISP1", 200),
            (2, 2, "AISP2", 200),
            (3, 3, "AISP3", 200),
            (4, 3, "AISP3", 200),
            (5, 3, "AISP3", 200),
            (6, 1, "AISP1", 201),
            (6, 2, "AISP2", 201)
        ]

        orgao_id_test = 1
        expected_output = ({1, 2}, {1, 2})

        get_aisps.cache_clear()
        output = get_orgaos_same_aisps(orgao_id_test)
        self.assertEqual(output, expected_output)

    def test_get_top_n_by_aisp(self):
        data_test = [(1, "PIP1", 50), (2, "PIP2", 30), (3, "PIP3", 40)]
        aisps_test = [1, 2]

        expected_output = [
            {"nm_pip": "Pip1", "valor_pip": 50},
            {"nm_pip": "Pip2", "valor_pip": 30},
        ]

        output = get_top_n_by_aisp(
            aisps_test,
            data_test,
            name_position=1,
            value_position=2,
            name_fieldname="nm_pip",
            value_fieldname="valor_pip",
        )

        self.assertEqual(output, expected_output)

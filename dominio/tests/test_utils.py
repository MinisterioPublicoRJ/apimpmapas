from django.test import TestCase

from dominio.utils import (
    format_text,
    get_value_given_key,
    get_top_n_orderby_value_as_dict
)


class UtilsTest(TestCase):
    def test_format_string(self):
        text = "PROMOTORIA DA CAPITAL"
        expected = "Promotoria da Capital"

        f_text = format_text(text)

        self.assertEqual(f_text, expected)

    def test_format_string_with_word_rio(self):
        text = "PROMOTORIA DO RIO DE JANEIRO"
        expected = "Promotoria do Rio de Janeiro"

        f_text = format_text(text)

        self.assertEqual(f_text, expected)

    def test_get_value_given_key(self):
        test_orgao_id = 42
        test_list = [
            (1, 'Nome1', 220),
            (10, 'Nome2', 140),
            (42, 'Nome3', 150),
            (60, 'Nome4', 65)
        ]
        output = get_value_given_key(
            test_list, test_orgao_id, key_position=0, value_position=2)
        expected_output = 150

        self.assertEqual(output, expected_output)

    def test_test_get_value_given_key_invalid_key(self):
        test_orgao_id = 33
        test_list = [
            (1, 'Nome1', 220),
            (10, 'Nome2', 140),
            (42, 'Nome3', 150),
            (60, 'Nome4', 65)
        ]
        output = get_value_given_key(
            test_list, test_orgao_id, key_position=0, value_position=2)
        expected_output = None

        self.assertEqual(output, expected_output)

    def test_get_top_n_orderby_value_as_dict(self):
        test_list = [
            (1, 'Nome1', 220, 0.5, 10),
            (10, 'Nome2', 140, 0.3, 5),
            (42, 'Nome3', 150, -0.10, 20),
            (60, 'Nome4', 65, 1.0, 2)
        ]
        output = get_top_n_orderby_value_as_dict(
            test_list,
            name_position=1,
            value_position=4,
            name_fieldname='nm_field',
            value_fieldname='value_field',
            n=3)
        expected_output = [
            {'nm_field': 'Nome3', 'value_field': 20},
            {'nm_field': 'Nome1', 'value_field': 10},
            {'nm_field': 'Nome2', 'value_field': 5}
        ]

        self.assertEqual(output, expected_output)

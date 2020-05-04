from django.test import TestCase

from dominio.utils import (
    format_text,
    get_value_given_key,
    get_top_n_orderby_value_as_dict,
    check_literal_eval,
    hbase_encode_row,
    hbase_decode_row,
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
            (1, "Nome1", 220),
            (10, "Nome2", 140),
            (42, "Nome3", 150),
            (60, "Nome4", 65)
        ]
        output = get_value_given_key(
            test_list, test_orgao_id, key_position=0, value_position=2)
        expected_output = 150

        self.assertEqual(output, expected_output)

    def test_test_get_value_given_key_invalid_key(self):
        test_orgao_id = 33
        test_list = [
            (1, "Nome1", 220),
            (10, "Nome2", 140),
            (42, "Nome3", 150),
            (60, "Nome4", 65)
        ]
        output = get_value_given_key(
            test_list, test_orgao_id, key_position=0, value_position=2)
        expected_output = None

        self.assertEqual(output, expected_output)

    def test_get_top_n_orderby_value_as_dict(self):
        test_list = [
            (1, "Nome1", 220, 0.5, 10),
            (10, "Nome2", 140, 0.3, 5),
            (42, "Nome3", 150, -0.10, 20),
            (60, "Nome4", 65, 1.0, 2)
        ]
        output = get_top_n_orderby_value_as_dict(
            test_list,
            name_position=1,
            value_position=4,
            name_fieldname="nm_field",
            value_fieldname="value_field",
            n=3)
        expected_output = [
            {"nm_field": "Nome3", "value_field": 20},
            {"nm_field": "Nome1", "value_field": 10},
            {"nm_field": "Nome2", "value_field": 5}
        ]

        self.assertEqual(output, expected_output)

    def test_check_literal_eval(self):
        x1 = "1"
        x2 = "[1, 2, 3]"
        x3 = "True"
        lit_x1 = check_literal_eval(x1)
        lit_x2 = check_literal_eval(x2)
        lit_x3 = check_literal_eval(x3)

        self.assertEqual(lit_x1, 1)
        self.assertEqual(lit_x2, [1, 2, 3])
        self.assertEqual(lit_x3, True)

    def test_check_literal_eval_exception(self):
        x1 = "Ola"
        lit_x1 = check_literal_eval(x1)

        self.assertEqual(lit_x1, x1)

    def test_hbase_decode(self):
        data = (b"k1", {b"c1": b"Nome", b"c2": b"True", b"c3": b"[1, 2, 3]"})
        expected_output = ("k1", {"c1": "Nome", "c2": True, "c3": [1, 2, 3]})
        decoded_data = hbase_decode_row(data)

        self.assertEqual(decoded_data, expected_output)

    def test_hbase_encode(self):
        expected_output = (
            b"k1",
            {b"c1": b"Nome", b"c2": b"True", b"c3": b"[1, 2, 3]"}
        )
        data = ("k1", {"c1": "Nome", "c2": True, "c3": [1, 2, 3]})
        decoded_data = hbase_encode_row(data)

        self.assertEqual(decoded_data, expected_output)

    def test_hbase_encode_decode(self):
        data = ("k1", {"c1": "Nome", "c2": True, "c3": [1, 2, 3]})

        encoded_data = hbase_encode_row(data)
        decoded_data = hbase_decode_row(encoded_data)

        self.assertEqual(data, decoded_data)

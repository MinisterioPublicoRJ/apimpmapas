from django.test import TestCase

from mprj_plus.forms import AreaForm, IconeForm, TemaForm


class FormTest(TestCase):
    def test_tema_form_valido(self):
        form = TemaForm({
            'titulo': 'titulo',
            'subtitulo': 'subtitulo',
            'fonte_dados': 'fonte'
        })

        self.assertTrue(form.is_valid())

    def test_tema_form_invalido(self):
        form = TemaForm({})

        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors, {
            'titulo': ['required'],
            'subtitulo': ['required'],
            'fonte_dados': ['required'],
        })

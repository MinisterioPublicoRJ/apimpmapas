from django.contrib.admin.sites import AdminSite
from unittest import mock, TestCase
import pytest

from dominio.admin import DocumentoAdmin
from dominio.models import Documento


@pytest.mark.django_db(transaction=True)
class TestDocumentoClasse(TestCase):
    def setUp(self):
        self.adminsite = AdminSite()
        self.classe_descr = 'classe'
        self.doc_class = mock.MagicMock(
            classe=mock.MagicMock(descricao=self.classe_descr)
        )
        self.doc_classless = mock.MagicMock(classe=None)
        self.classless_msg = 'SEM CLASSE DEFINIDA'

    def test_document_classes(self):
        self.docto_admin = DocumentoAdmin(
            Documento,
            self.adminsite
        )
        classed = self.docto_admin.get_classe(self.doc_class)
        classless = self.docto_admin.get_classe(self.doc_classless)

        self.assertEqual(classed, self.classe_descr)
        self.assertEqual(classless, self.classless_msg)

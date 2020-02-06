from django.contrib.admin.sites import AdminSite
from model_mommy.mommy import make
from unittest import TestCase
import pytest

from dominio.admin import DocumentoAdmin
from dominio.models import Documento


@pytest.mark.django_db(transaction=True)
class TestDocumentoClasse(TestCase):
    def setUp(self):
        self.adminsite = AdminSite()
        self.classe = make('dominio.DoctoClasse', descricao='classe')
        self.doc_class = make('dominio.Documento', classe=self.classe)
        self.doc_classless = make('dominio.Documento', classe=None)
        self.classless_msg = 'SEM CLASSE DEFINIDA'

    def test_document_classes(self):
        self.docto_admin = DocumentoAdmin(
            Documento,
            self.adminsite
        )
        classed = self.docto_admin.get_classe(self.doc_class)
        classless = self.docto_admin.get_classe(self.doc_classless)

        self.assertEqual(classed, self.classe.descricao)
        self.assertEqual(classless, self.classless_msg)

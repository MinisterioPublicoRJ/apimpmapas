from datetime import datetime

from cached_property import cached_property
from docxtpl import DocxTemplate

from dominio.documentos.dao import MinutaPrescricaoDAO


# TODO: criar testes
class MinutaPrescricaoController:
    template = "dominio/documentos/doc_templates/minuta - prescricao.docx"

    def __init__(self, docu_dk, matricula):
        self.docu_dk = docu_dk
        self.matricula = matricula

    @cached_property
    def context(self):
        context = {
            "matricula_promotor": self.matricula,
            "data_hoje": datetime.now()
        }

        context.update(MinutaPrescricaoDAO.get(docu_dk=self.docu_dk))
        return context

    def render(self, response):
        doc = DocxTemplate(self.template)
        doc.render(self.context)
        doc.save(response)

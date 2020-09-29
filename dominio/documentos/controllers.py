from cached_property import cached_property
from docxtpl import DocxTemplate


# TODO: criar testes
class MinutaPrescricaoController:
    template = "dominio/documentos/doc_templates/minuta - prescricao.docx"

    def __init__(self, docu_dk):
        self.docu_dk = docu_dk

    @cached_property
    def context(self):
        return {'data_hoje': '28 de setembro de 2020'}

    def render(self, response):
        doc = DocxTemplate(self.template)
        doc.render(self.context)
        doc.save(response)

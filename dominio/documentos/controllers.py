from cached_property import cached_property
from django.http import HttpResponse
from docxtpl import DocxTemplate


# TODO: criar testes
class MinutaPrescricaoController:
    template = "dominio/documentos/doc_templates/minuta - prescricao.docx"

    def __init__(self, response: HttpResponse):
        self.response = response

    @cached_property
    def context(self):
        return {'data_hoje': '28 de setembro de 2020'}

    def render(self):
        doc = DocxTemplate(self.template)
        doc.render(self.context)
        doc.save(self.response)
        return self.response

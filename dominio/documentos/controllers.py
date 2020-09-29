import locale
from datetime import date

from cached_property import cached_property
from docxtpl import DocxTemplate

from dominio.documentos.dao import MinutaPrescricaoDAO


class MinutaPrescricaoController:
    template = "dominio/documentos/doc_templates/minuta - prescricao.docx"

    def __init__(self, docu_dk, matricula):
        self.docu_dk = docu_dk
        self.matricula = matricula

    def get_preposicao(self, comarca):
        preposicoes = {
            "CAPITAL": "da",
            "RIO DE JANEIRO": "do",
        }
        return preposicoes.get(comarca, "de").upper()

    @cached_property
    def context(self):
        locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')
        context = {
            "matricula_promotor": self.matricula,
            "data_hoje": date.today().strftime('%d de %B de %Y')
        }
        context.update(MinutaPrescricaoDAO.get(docu_dk=self.docu_dk))
        context["preposicao_comarca"] = self.get_preposicao(
            context["comarca_tj"]
        )

        return context

    def render(self, response):
        doc = DocxTemplate(self.template)
        doc.render(self.context)
        doc.save(response)

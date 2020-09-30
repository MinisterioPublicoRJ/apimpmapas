import locale
from datetime import date

from cached_property import cached_property
from docxtpl import DocxTemplate

from dominio.documentos.dao import DadosUsuarioDAO, MinutaPrescricaoDAO


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

    def corrige_comarca(self, comarca):
        return "CAPITAL" if comarca == "RIO DE JANEIRO" else comarca

    def get_responsavel(self, orgao, matricula):
        logado = DadosUsuarioDAO.get(matricula)
        # TODO Aqui iremos checar se ele é um 'PROMOTOR DE JUSTICA' e se
        # não for, pegar o promotor responsavel pela promotoria do documento

        return logado

    @cached_property
    def context(self):
        locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')
        context = {"data_hoje": date.today().strftime('%d de %B de %Y')}
        context.update(MinutaPrescricaoDAO.get(docu_dk=self.docu_dk))
        context.update(self.get_responsavel(
            orgao=context.get('orgao_responsavel'),
            matricula=self.matricula
        ))
        context["comarca_tj"] = self.corrige_comarca(context["comarca_tj"])
        context["preposicao_comarca"] = self.get_preposicao(
            context["comarca_tj"]
        )
        context['data_fato'] = context['data_fato'].strftime('%d de %B de %Y')

        return context

    def render(self, response):
        doc = DocxTemplate(self.template)
        doc.render(self.context)
        doc.save(response)

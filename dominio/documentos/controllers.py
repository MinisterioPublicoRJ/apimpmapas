import locale
from datetime import date

from cached_property import cached_property
from docxtpl import DocxTemplate

from dominio.documentos.dao import (
    DadosPromotorDAO,
    DadosUsuarioDAO,
    MinutaPrescricaoDAO
)

class MinutaPrescricaoController:
    template = "dominio/documentos/doc_templates/minuta - prescricao.docx"

    def __init__(self, orgao_id, docu_dk, cpf):
        self.orgao_id = orgao_id
        self.docu_dk = docu_dk
        self.cpf = cpf

    def get_preposicao(self, comarca):
        preposicoes = {
            "CAPITAL": "da",
            "RIO DE JANEIRO": "do",
        }
        return preposicoes.get(comarca, "de").upper()

    def corrige_comarca(self, comarca):
        return "CAPITAL" if comarca == "RIO DE JANEIRO" else comarca

    @cached_property
    def get_responsavel(self):
        return DadosPromotorDAO.get(cpf=self.cpf)

    def get_delitos(self):
        lista_assuntos = DadosAssuntoDAO.get(docu_dk=self.docu_dk)
        delitos = []
        alteracao = 1
        for assunto in lista_assuntos:
            if assunto.get("multiplicador") == 1:
                alteracao *= assunto.get("max_pena")
            else:
                delitos.append(assunto)

        result = {
            "nome_delito": "",
            "lei_delito": "",
            "max_pena": "",
        }
        for delito in delitos:
            #TODO concatenar os delitos em result

        return result
        

    @cached_property
    def context(self):
        locale.setlocale(locale.LC_ALL, "pt_BR.UTF-8")
        context = {"data_hoje": date.today().strftime("%d de %B de %Y")}
        context.update(MinutaPrescricaoDAO.get(docu_dk=self.docu_dk))
        context.update(self.get_delitos())
        promotor = self.get_responsavel()
        context.update(
            self.get_responsavel(
                matricula_promotor=promotor.get("matricula_promotor"),
                nome_promotor=promotor.get("nome_promotor")
            )
        )
        context["comarca_tj"] = self.corrige_comarca(context["comarca_tj"])
        context["preposicao_comarca"] = self.get_preposicao(
            context["comarca_tj"]
        )
        context["data_fato"] = context["data_fato"].strftime("%d de %B de %Y")

        return context

    def render(self, response):
        doc = DocxTemplate(self.template)
        doc.render(self.context)
        doc.save(response)

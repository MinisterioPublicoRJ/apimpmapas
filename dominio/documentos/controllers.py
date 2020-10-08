import abc
from datetime import date

from cached_property import cached_property
from docxtpl import DocxTemplate

from dominio.documentos.dao import (
    DadosAssuntoDAO,
    DadosPromotorDAO,
    MinutaPrescricaoDAO
)
from dominio.documentos.helpers import formata_lista, formata_pena, traduz_mes


class BaseDocumentoController(metaclass=abc.ABCMeta):
    template = None

    def __init__(self, orgao_id, docu_dk, cpf):
        self.orgao_id = orgao_id
        self.docu_dk = docu_dk
        self.cpf = cpf

    @abc.abstractproperty
    def context(self):
        pass

    def render(self, response):
        doc = DocxTemplate(self.template)
        doc.render(self.context)
        doc.save(response)


class MinutaPrescricaoController(BaseDocumentoController):
    template = "dominio/documentos/doc_templates/minuta_prescricao.docx"

    def get_preposicao(self, comarca):
        preposicoes = {
            "CAPITAL": "da",
            "RIO DE JANEIRO": "do",
        }
        return preposicoes.get(comarca, "de").upper()

    def corrige_comarca(self, comarca):
        return "CAPITAL" if comarca == "RIO DE JANEIRO" else comarca

    @cached_property
    def responsavel(self):
        return DadosPromotorDAO.get(cpf=self.cpf)

    @cached_property
    def delitos(self):
        # TODO: talvez levar esse código para o DAO. Pode ser que não seja
        # responsabilidade do Controller saber como o dado é preparado.
        lista_assuntos = DadosAssuntoDAO.get(docu_dk=self.docu_dk)
        delitos = []
        alteracao = 1
        for assunto in lista_assuntos:
            if assunto.get("multiplicador") == 1:
                alteracao *= assunto.get("max_pena")
            else:
                delitos.append(assunto)

        result = {}
        result["nome_delito"] = formata_lista(
            [item["nome_delito"] for item in delitos]
        )
        result["lei_delito"] = formata_lista(
            [item["lei_delito"] for item in delitos]
        )
        result["max_pena"] = formata_lista(
            [
                str(formata_pena(item["max_pena"] * alteracao))
                for item in delitos
            ]
        )

        return result

    @cached_property
    def context(self):
        context = {
            "data_hoje": traduz_mes(date.today().strftime("%d de %B de %Y"))
        }
        context.update(MinutaPrescricaoDAO.get(docu_dk=self.docu_dk))
        context.update(self.delitos)
        context.update(self.responsavel)
        context["comarca_tj"] = self.corrige_comarca(context["comarca_tj"])
        context["preposicao_comarca"] = self.get_preposicao(
            context["comarca_tj"]
        )
        context["data_fato"] = traduz_mes(
            context["data_fato"].strftime("%d de %B de %Y")
        )

        return context


class ProrrogacaoICController(BaseDocumentoController):
    @cached_property
    def context(self):
        return {"context": 1}

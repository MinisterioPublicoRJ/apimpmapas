from django.http import FileResponse, HttpResponse
from django.shortcuts import Http404
from django.views.generic import View

from dominio.documentos.controllers import (
    InstauracaoICController,
    MinutaPrescricaoController,
    ProrrogacaoICController,
    ProrrogacaoPPController,
)
from dominio.documentos.dao import ListaROsAusentesDAO
from dominio.documentos.helpers import gera_planilha_excel, ros_ausentes

from dominio.exceptions import APIEmptyResultError
from dominio.mixins import JWTAuthMixin


class BaseDocumentoViewMixin:
    attachment_name = None

    def create_response(self):
        content_type = (
            'application/vnd.openxmlformats-officedocument.'
            'wordprocessingml.document'
        )
        response = HttpResponse(content_type=content_type)
        response['Content-Disposition'] = (
            "attachment;"
            f"filename={self.attachment_name}"
        )
        return response


class MinutaPrescricaoView(BaseDocumentoViewMixin, JWTAuthMixin, View):
    attachment_name = "minuta-prescricao.docx"

    def get(self, request, *args, **kwargs):
        orgao_id = kwargs.get(self.orgao_url_kwarg)
        docu_dk = kwargs.get("docu_dk")
        cpf = kwargs.get("cpf")
        controller = MinutaPrescricaoController(
            orgao_id=orgao_id,
            docu_dk=docu_dk,
            cpf=cpf
        )
        response = self.create_response()
        try:
            controller.render(response)
        except APIEmptyResultError:
            raise Http404

        return response


class ProrrogacaoICView(BaseDocumentoViewMixin, JWTAuthMixin, View):
    attachment_name = "prorrogacao-ic.docx"

    def get(self, request, *args, **kwargs):
        response = self.create_response()

        orgao_id = kwargs.get(self.orgao_url_kwarg)
        docu_dk = kwargs.get("docu_dk")
        cpf = kwargs.get("cpf")
        controller = ProrrogacaoICController(
            orgao_id=orgao_id,
            cpf=cpf,
            docu_dk=docu_dk,
        )
        try:
            controller.render(response)
        except APIEmptyResultError:
            raise Http404

        return response


class ProrrogacaoPPView(BaseDocumentoViewMixin, JWTAuthMixin, View):
    attachment_name = "prorrogacao-pp.docx"

    def get(self, request, *args, **kwargs):
        response = self.create_response()

        orgao_id = kwargs.get(self.orgao_url_kwarg)
        docu_dk = kwargs.get("docu_dk")
        cpf = kwargs.get("cpf")
        controller = ProrrogacaoPPController(
            orgao_id=orgao_id,
            cpf=cpf,
            docu_dk=docu_dk,
        )
        try:
            controller.render(response)
        except APIEmptyResultError:
            raise Http404

        return response


class InstauracaoICView(BaseDocumentoViewMixin, JWTAuthMixin, View):
    attachment_name = "instauracao-ic.docx"

    def get(self, request, *args, **kwargs):
        response = self.create_response()

        orgao_id = kwargs.get(self.orgao_url_kwarg)
        docu_dk = kwargs.get("docu_dk")
        cpf = kwargs.get("cpf")
        controller = InstauracaoICController(
            orgao_id=orgao_id,
            cpf=cpf,
            docu_dk=docu_dk,
        )
        try:
            controller.render(response)
        except APIEmptyResultError:
            raise Http404

        return response


class ListaROsAusentesView(JWTAuthMixin, View):
    def get(self, request, *args, **kwargs):
        num_delegacia = kwargs.get("num_delegacia")
        header = ["id", "Número procedimento"]

        lista_ros = ListaROsAusentesDAO.get(num_delegacia=num_delegacia)
        return FileResponse(
            gera_planilha_excel(
                ros_ausentes(lista_ros, num_delegacia),
                header=header,
                sheet_title="ROs Ausentes"
            ),
            filename="ros-ausentes.xlsx",
            as_attachment=True
        )

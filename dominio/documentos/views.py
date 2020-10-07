from django.http import HttpResponse
from django.views.generic import View

from dominio.documentos.controllers import MinutaPrescricaoController
from dominio.mixins import JWTAuthMixin


class MinutaPrescricaoView(JWTAuthMixin, View):
    attachment_name = "minuta-prescricao.docx"

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
        controller.render(response)
        return response

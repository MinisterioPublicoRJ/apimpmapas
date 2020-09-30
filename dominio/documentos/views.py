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
        docu_dk = int(kwargs.get("docu_dk"))
        controller = MinutaPrescricaoController(docu_dk, self.token_payload)
        response = self.create_response()
        controller.render(response)
        return response

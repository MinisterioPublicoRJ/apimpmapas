from django.http import HttpResponse
from django.views.generic import View

from dominio.documentos.controllers import MinutaPrescricaoController
from dominio.mixins import JWTAuthMixin


class MinutaPrescricaoView(JWTAuthMixin, View):
    def get(self, request, *args, **kwargs):
        docu_dk = kwargs.get("docu_dk")
        matricula = self.token_payload.get("matricula")
        content_type = (
            'application/vnd.openxmlformats-officedocument.'
            'wordprocessingml.document'
        )
        response = HttpResponse(content_type=content_type)
        response['Content-Disposition'] = (
            'attachment;'
            'filename=minuta-prescricao.docx'
        )
        controller = MinutaPrescricaoController(docu_dk, matricula)
        controller.render(response)
        return response

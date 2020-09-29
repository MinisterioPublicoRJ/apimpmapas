from django.http import HttpResponse
from django.views.generic import View

from dominio.documentos.controllers import MinutaPrescricaoController


class MinutaPrescricaoView(View):
    def get(self, request, *args, **kwargs):
        docu_dk = kwargs.get("docu_dk")
        content_type = (
            'application/vnd.openxmlformats-officedocument.'
            'wordprocessingml.document'
        )
        response = HttpResponse(content_type=content_type)
        response['Content-Disposition'] = (
            'attachment;'
            'filename=minuta-prescricao.docx'
        )
        controller = MinutaPrescricaoController(docu_dk)
        controller.render(response)
        return response

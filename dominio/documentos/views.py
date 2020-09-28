from django.http import HttpResponse
from django.views.generic import View

from dominio.documentos.controllers import MinutaPrescricaoController


class MinutaPrescricaoView(View):
    def get(self, request, *args, **kwargs):
        mime_type = (
            'application/vnd.openxmlformats-officedocument.'
            'wordprocessingml.document'
        )
        response = HttpResponse(content_type=mime_type)
        response['Content-Disposition'] = (
            'attachment;'
            'filename=minuta-prescricao.docx'
        )
        controller = MinutaPrescricaoController(response)
        return controller.render()

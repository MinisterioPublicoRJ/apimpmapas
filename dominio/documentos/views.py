from django.http import HttpResponse
from django.views.generic import View
from docxtpl import DocxTemplate

class MinutaPrescricaoView(View):
    
    def get(self, request, *args, **kwargs):
        template = 'minuta - prescricao - V1.docx'
        context = {'data_hoje': '28 de setembro de 2020'}
        mime_type = 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'

        doc = DocxTemplate(template)
        doc.render(context)
        response = HttpResponse(content_type=mime_type)
        response['Content-Disposition'] = 'attachment; filename=minuta-prescricao.docx'
        doc.save(response)
        return response
        

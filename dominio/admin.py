from django.contrib import admin

from .models import Documento, Usuario

# Register your models here.
@admin.register(Documento)
class DocumentoAdmin(admin.ModelAdmin):
    list_display = ('num_mp', 'get_classe')
    fields = ('num_mp', 'classe')

    def get_classe(self, obj):
        if obj.classe:
            return obj.classe.descricao
        return 'SEM CLASSE DEFINIDA'


admin.site.register(Usuario)

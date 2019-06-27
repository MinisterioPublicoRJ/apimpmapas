from django.contrib import admin

from api.models import (
    EntidadeModel,
    TipoEntidadeModel,
    TipoDadoModel,
    DadoModel
)


admin.site.register(TipoEntidadeModel)
admin.site.register(TipoDadoModel)
admin.site.register(EntidadeModel)
admin.site.register(DadoModel)

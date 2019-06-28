from django.contrib import admin

from api.models import (
    Entidade,
    TipoEntidade,
    TipoDado,
    Dado
)


admin.site.register(TipoEntidade)
admin.site.register(TipoDado)
admin.site.register(Entidade)
admin.site.register(Dado)

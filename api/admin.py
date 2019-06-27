from django.contrib import admin

from api.models import EntidadeModel, TipoEntidadeModel


admin.site.register(TipoEntidadeModel)
admin.site.register(EntidadeModel)

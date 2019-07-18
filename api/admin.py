from django.contrib import admin

from api.models import Entidade, Dado, Icone, TipoEntidade


admin.site.register(Entidade)
admin.site.register(Dado)
admin.site.register(Icone)
admin.site.register(TipoEntidade)

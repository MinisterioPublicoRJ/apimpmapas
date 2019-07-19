from django.contrib import admin
from ordered_model.admin import OrderedModelAdmin

from api.models import Dado, Icone, Entidade


class DadoAdmin(OrderedModelAdmin):
    list_display = ('title', 'entity_type', 'move_up_down_links')
    list_filter = ('entity_type__name',)


admin.site.register(Dado, DadoAdmin)
admin.site.register(Icone)
admin.site.register(Entidade)

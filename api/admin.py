from django.contrib import admin
from ordered_model.admin import OrderedModelAdmin

from api.models import Dado, Icone, Entidade


@admin.register(Entidade)
class EntidadeAdmin(admin.ModelAdmin):
    list_display = ('name', 'abreviation')
    fieldsets = (
        (None, {
            'fields': ('name', 'abreviation')
        }),
        ('Dados principais', {
            'fields': (
                'database',
                'schema',
                'table',
                'id_column',
                'name_column')
        }),
        ('Mapa', {
            'classes': ('collapse', ),
            'fields': (
                'database_mapa',
                'schema_mapa',
                'table_mapa',
                'id_column_mapa',
                'name_column_mapa',
                'geom_column_mapa')
        })
    )


@admin.register(Dado)
class DadoAdmin(OrderedModelAdmin):
    list_display = ('title', 'entity_type', 'move_up_down_links')
    list_filter = ('entity_type__name',)


admin.site.register(Icone)

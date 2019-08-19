from django.contrib import admin
from django import forms
from ordered_model.admin import OrderedModelAdmin

from .models import (
    Dado,
    Icone,
    Entidade,
    Mapa,
    TipoDado,
    TemaDado,
    ColunaDado
)


class MapaAdminInline(admin.StackedInline):
    model = Mapa


class ColunaDadoForm(forms.ModelForm):
    info_type = forms.ChoiceField(
        choices=ColunaDado.INFO_CHOICES,
        help_text=ColunaDado.help_info_type
    )


class ColunaDadoAdminInline(admin.TabularInline):
    model = ColunaDado
    form = ColunaDadoForm


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
        })
    )
    inlines = [MapaAdminInline]


@admin.register(Dado)
class DadoAdmin(OrderedModelAdmin):
    list_display = ('title', 'entity_type', 'theme', 'move_up_down_links')
    list_filter = ('entity_type__name',)
    fieldsets = (
        (None, {
            'fields': (
                'title',
                'data_type',
                'entity_type',
                'theme',
                'icon'
            )
        }),
        ('Dados exibidos', {
            'fields': (
                'database',
                'schema',
                'table',
                'id_column',
                'data_column',
                'label_column',
                'source_column',
                'details_column',
                'image_column',
                'external_link_column',
                'entity_link_type',
                'entity_link_id_column')
        })
    )
    inlines = [ColunaDadoAdminInline]


admin.site.register(Icone)
admin.site.register(TipoDado)
admin.site.register(TemaDado)
